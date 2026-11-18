import pytest
from django.urls import reverse
from rest_framework import status

from adhocracy4.polls.models import Answer
from adhocracy4.polls.models import OtherVote
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


@pytest.mark.django_db
def test_existing_answer_of_mandatory_question_stays_valid_when_changing_another_answer(
    user, apiclient, poll_factory, question_factory, choice_factory
):
    """The a4 client only submits the questions that were changed."""
    poll = poll_factory()
    mandatory_question = question_factory(poll=poll, is_mandatory=True)
    mandatory_choice = choice_factory(question=mandatory_question)
    optional_question = question_factory(poll=poll)
    optional_choice = choice_factory(question=optional_question)
    new_optional_choice = choice_factory(question=optional_question)

    apiclient.force_authenticate(user=user)

    data = {
        "votes": {
            mandatory_question.pk: {
                "choices": [mandatory_choice.pk],
                "other_choice_answer": "",
                "open_answer": "",
            },
            optional_question.pk: {
                "choices": [optional_choice.pk],
                "other_choice_answer": "",
                "open_answer": "",
            },
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

        # only the optional question is part of the second request
        data = {
            "votes": {
                optional_question.pk: {
                    "choices": [new_optional_choice.pk],
                    "other_choice_answer": "",
                    "open_answer": "",
                }
            }
        }
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Vote.objects.filter(choice=mandatory_choice, creator=user).exists()
    assert Vote.objects.filter(choice=new_optional_choice, creator=user).exists()


@pytest.mark.django_db
def test_removing_the_answer_of_a_mandatory_question_is_rejected(
    user, apiclient, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    mandatory_question = question_factory(poll=poll, is_mandatory=True)
    mandatory_choice = choice_factory(question=mandatory_question)

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

        data = {
            "votes": {
                mandatory_question.pk: {
                    "choices": [],
                    "other_choice_answer": "",
                    "open_answer": "",
                }
            }
        }
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Vote.objects.filter(choice=mandatory_choice, creator=user).exists()


@pytest.mark.django_db
def test_admin_update_without_is_mandatory_keeps_the_value(
    apiclient, admin, poll_factory, question_factory, choice_factory
):
    """Older clients do not send the new field and must not reset it."""
    poll = poll_factory()
    question = question_factory(poll=poll, is_mandatory=True)
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
@pytest.mark.parametrize("votes", [None, [], "invalid"])
def test_vote_with_invalid_votes_payload_returns_400(
    user, apiclient, poll_factory, votes
):
    poll = poll_factory()
    apiclient.force_authenticate(user=user)

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), {"votes": votes}, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_vote_without_votes_payload_returns_400(user, apiclient, poll_factory):
    poll = poll_factory()
    apiclient.force_authenticate(user=user)

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), {}, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_stored_whitespace_open_answer_does_not_count(
    user, apiclient, poll_factory, question_factory, open_question_factory, choice_factory
):
    poll = poll_factory()
    mandatory_question = open_question_factory(poll=poll, is_mandatory=True)
    optional_question = question_factory(poll=poll)
    optional_choice = choice_factory(question=optional_question)
    Answer.objects.create(question=mandatory_question, answer="   ", creator=user)

    apiclient.force_authenticate(user=user)

    data = {
        "votes": {
            optional_question.pk: {
                "choices": [optional_choice.pk],
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert str(mandatory_question.pk) in response.data


@pytest.mark.django_db
def test_stored_open_answer_counts_when_question_is_omitted(
    user, apiclient, poll_factory, question_factory, open_question_factory, choice_factory
):
    poll = poll_factory()
    mandatory_question = open_question_factory(poll=poll, is_mandatory=True)
    optional_question = question_factory(poll=poll)
    optional_choice = choice_factory(question=optional_question)
    Answer.objects.create(
        question=mandatory_question, answer="my answer", creator=user
    )

    apiclient.force_authenticate(user=user)

    data = {
        "votes": {
            optional_question.pk: {
                "choices": [optional_choice.pk],
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_stored_other_answer_without_text_does_not_count(
    user, apiclient, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    mandatory_question = question_factory(poll=poll, is_mandatory=True)
    choice_factory(question=mandatory_question)
    other_choice = choice_factory(question=mandatory_question, is_other_choice=True)
    vote = Vote.objects.create(choice=other_choice, creator=user)
    OtherVote.objects.create(vote=vote, answer="   ")

    optional_question = question_factory(poll=poll)
    optional_choice = choice_factory(question=optional_question)

    apiclient.force_authenticate(user=user)

    data = {
        "votes": {
            optional_question.pk: {
                "choices": [optional_choice.pk],
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert str(mandatory_question.pk) in response.data


@pytest.mark.django_db
def test_mandatory_other_choice_with_padded_id_and_blank_text_is_rejected(
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
                "choices": ["0" + str(other_choice.pk)],
                "other_choice_answer": " ",
                "open_answer": "",
            }
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_numeric_open_answer_is_rejected(
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
                "open_answer": 123,
            }
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_numeric_choices_are_rejected(
    user, apiclient, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    question = question_factory(poll=poll, is_mandatory=True)
    choice_factory(question=question)

    apiclient.force_authenticate(user=user)

    data = {
        "votes": {
            question.pk: {
                "choices": 1,
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_numeric_other_answer_is_rejected(
    user, apiclient, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    question = question_factory(poll=poll, is_mandatory=True)
    choice = choice_factory(question=question)
    choice_factory(question=question, is_other_choice=True)

    apiclient.force_authenticate(user=user)

    data = {
        "votes": {
            question.pk: {
                "choices": [choice.pk],
                "other_choice_answer": 42,
                "open_answer": "",
            }
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_failed_vote_rolls_back_all_answers(
    user, apiclient, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    mandatory_question = question_factory(poll=poll, is_mandatory=True)
    mandatory_choice = choice_factory(question=mandatory_question)
    broken_question = question_factory(poll=poll)
    choice_factory(question=broken_question)

    apiclient.force_authenticate(user=user)

    data = {
        "votes": {
            mandatory_question.pk: {
                "choices": [mandatory_choice.pk],
                "other_choice_answer": "",
                "open_answer": "",
            },
            broken_question.pk: {
                "choices": [999999],
                "other_choice_answer": "",
                "open_answer": "",
            },
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(vote_url(poll), data, format="json")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Vote.objects.count() == 0


@pytest.mark.django_db
def test_admin_update_with_string_id_keeps_question_and_votes(
    apiclient, admin, user, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    question = question_factory(poll=poll, is_mandatory=True)
    choice = choice_factory(question=question)
    choice_factory(question=question)
    vote = Vote.objects.create(choice=choice, creator=user)

    apiclient.force_authenticate(user=admin)
    data = {
        "questions": [
            {
                "id": str(question.pk),
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
    assert Question.objects.filter(pk=question.pk).exists()
    assert Vote.objects.filter(pk=vote.pk).exists()
    question.refresh_from_db()
    assert question.is_mandatory is True


@pytest.mark.django_db
def test_admin_cannot_make_question_without_choices_mandatory(
    apiclient, admin, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    question = question_factory(poll=poll)
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
                "choices": [],
            }
        ]
    }

    response = apiclient.put(
        reverse("polls-detail", kwargs={"pk": poll.pk}), data, format="json"
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    question.refresh_from_db()
    assert question.is_mandatory is False


@pytest.mark.django_db
def test_other_answer_text_is_saved(
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
    other_vote = OtherVote.objects.get(vote__choice=other_choice)
    assert other_vote.answer == "my other answer"
