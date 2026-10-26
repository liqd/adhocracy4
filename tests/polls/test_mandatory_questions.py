import pytest
from django.urls import reverse
from rest_framework import status

from adhocracy4.polls.models import Answer
from adhocracy4.polls.models import Question
from adhocracy4.polls.models import Vote
from adhocracy4.polls.phases import VotingPhase
from tests.helpers import active_phase


def vote_url(poll):
    return reverse("polls-vote", kwargs={"pk": poll.pk})


@pytest.mark.django_db
def test_question_is_mandatory_defaults_to_false(question_factory, poll_factory):
    poll = poll_factory()
    question = question_factory(poll=poll)

    assert question.is_mandatory is False
    assert Question._meta.get_field("is_mandatory").default is False


@pytest.mark.django_db
def test_is_mandatory_in_poll_response(apiclient, poll_factory, question_factory):
    poll = poll_factory()
    question_factory(poll=poll, is_mandatory=True)

    apiclient.force_authenticate(user=poll.creator)
    response = apiclient.get(
        reverse("polls-detail", kwargs={"pk": poll.pk}), format="json"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["questions"][0]["is_mandatory"] is True


@pytest.mark.django_db
def test_admin_can_update_is_mandatory(
    apiclient, admin, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    question = question_factory(poll=poll)
    choice = choice_factory(question=question)
    choice_factory(question=question)

    apiclient.force_authenticate(user=admin)
    data = {
        "questions": [
            {
                "id": question.pk,
                "label": question.label,
                "help_text": "",
                "multiple_choice": False,
                "is_open": False,
                "is_mandatory": True,
                "choices": [
                    {"id": choice.pk, "label": choice.label, "is_other_choice": False},
                    {"label": "another choice", "is_other_choice": False},
                ],
            }
        ]
    }

    response = apiclient.put(
        reverse("polls-detail", kwargs={"pk": poll.pk}), data, format="json"
    )

    assert response.status_code == status.HTTP_200_OK
    question.refresh_from_db()
    assert question.is_mandatory is True


@pytest.mark.django_db
def test_vote_rejected_for_unanswered_mandatory_question(
    user, apiclient, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    question = question_factory(poll=poll, is_mandatory=True)
    choice_factory(question=question)
    choice_factory(question=question)

    apiclient.force_authenticate(user=user)

    data = {"votes": {}}

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert str(question.pk) in response.data
    assert Vote.objects.count() == 0


@pytest.mark.django_db
def test_vote_rejected_for_unanswered_mandatory_single_choice_question(
    user, apiclient, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    question = question_factory(poll=poll, is_mandatory=True)
    choice_factory(question=question)

    apiclient.force_authenticate(user=user)

    data = {
        "votes": {
            question.pk: {
                "choices": [],
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Vote.objects.count() == 0


@pytest.mark.django_db
def test_vote_accepted_for_answered_mandatory_question(
    user, apiclient, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    question = question_factory(poll=poll, is_mandatory=True)
    choice = choice_factory(question=question)

    apiclient.force_authenticate(user=user)

    data = {
        "votes": {
            question.pk: {
                "choices": [choice.pk],
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Vote.objects.count() == 1


@pytest.mark.django_db
def test_vote_rejected_for_unanswered_mandatory_multiple_choice_question(
    user, apiclient, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    question = question_factory(poll=poll, multiple_choice=True, is_mandatory=True)
    choice_factory(question=question)
    choice_factory(question=question)

    apiclient.force_authenticate(user=user)

    data = {
        "votes": {
            question.pk: {
                "choices": [],
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Vote.objects.count() == 0


@pytest.mark.django_db
def test_vote_rejected_for_blank_mandatory_open_question(
    user, apiclient, poll_factory, open_question_factory
):
    poll = poll_factory()
    question = open_question_factory(poll=poll, is_mandatory=True)

    apiclient.force_authenticate(user=user)

    data = {
        "votes": {
            question.pk: {
                "choices": [],
                "other_choice_answer": "",
                "open_answer": "   ",
            }
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Answer.objects.count() == 0


@pytest.mark.django_db
def test_vote_accepted_for_answered_mandatory_open_question(
    user, apiclient, poll_factory, open_question_factory
):
    poll = poll_factory()
    question = open_question_factory(poll=poll, is_mandatory=True)

    apiclient.force_authenticate(user=user)

    data = {
        "votes": {
            question.pk: {
                "choices": [],
                "other_choice_answer": "",
                "open_answer": "my answer",
            }
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Answer.objects.count() == 1


@pytest.mark.django_db
def test_vote_rejected_for_mandatory_other_choice_without_text(
    user, apiclient, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    question = question_factory(poll=poll, is_mandatory=True)
    choice_factory(question=question)
    other_choice = choice_factory(question=question, is_other_choice=True)

    apiclient.force_authenticate(user=user)

    data = {
        "votes": {
            question.pk: {
                "choices": [other_choice.pk],
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Vote.objects.count() == 0


@pytest.mark.django_db
def test_vote_accepted_for_mandatory_other_choice_with_text(
    user, apiclient, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    question = question_factory(poll=poll, multiple_choice=True, is_mandatory=True)
    choice = choice_factory(question=question)
    other_choice = choice_factory(question=question, is_other_choice=True)

    apiclient.force_authenticate(user=user)

    data = {
        "votes": {
            question.pk: {
                "choices": [choice.pk, other_choice.pk],
                "other_choice_answer": "my other answer",
                "open_answer": "",
            }
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Vote.objects.count() == 2


@pytest.mark.django_db
def test_optional_question_can_stay_unanswered(
    user, apiclient, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    mandatory_question = question_factory(poll=poll, is_mandatory=True)
    mandatory_choice = choice_factory(question=mandatory_question)
    question_factory(poll=poll)

    apiclient.force_authenticate(user=user)

    data = {
        "votes": {
            mandatory_question.pk: {
                "choices": [mandatory_choice.pk],
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
