from unittest.mock import patch

import pytest
from django.test import override_settings
from django.urls import reverse
from rest_framework import status

from adhocracy4.polls.models import Answer
from adhocracy4.polls.models import OtherVote
from adhocracy4.polls.models import Vote
from adhocracy4.polls.phases import VotingPhase
from tests.apps.organisations.models import OrganisationTermsOfUse
from tests.helpers import active_phase


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
@patch("adhocracy4.polls.api.reverse", return_value="/")
def test_agreement_save_with_admin_vote(
    mock_provider, admin, apiclient, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    assert Vote.objects.count() == 0

    apiclient.force_authenticate(user=admin)

    url = reverse("polls-vote", kwargs={"pk": poll.pk})

    data = {
        "votes": {
            question.pk: {
                "choices": [choice1.pk],
                "other_choice_answer": "",
                "open_answer": "",
            }
        },
        "agreed_terms_of_use": True,
    }

    response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Vote.objects.count() == 1
    terms = OrganisationTermsOfUse.objects.all()
    assert len(terms) == 1
    assert terms[0].user == admin


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
@patch("adhocracy4.polls.api.reverse", return_value="/")
def test_agreement_save_with_vote(
    mock_provider, user, apiclient, poll_factory, question_factory, choice_factory
):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)
    open_question = question_factory(poll=poll, is_open=True)

    assert Vote.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse("polls-vote", kwargs={"pk": poll.pk})

    data = {
        "votes": {
            question.pk: {
                "choices": [choice1.pk],
                "other_choice_answer": "",
                "open_answer": "",
            },
            open_question.pk: {
                "choices": [],
                "other_choice_answer": "",
                "open_answer": "an open answer",
            },
        },
        "agreed_terms_of_use": True,
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1
    assert Answer.objects.count() == 1
    terms = OrganisationTermsOfUse.objects.all()
    assert len(terms) == 1
    assert terms[0].user == user


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
@patch("adhocracy4.polls.api.reverse", return_value="/")
def test_unregistered_user_can_vote_with_agreement(
    mock_provider, apiclient, poll_factory, question_factory, choice_factory
):

    poll = poll_factory()
    poll.allow_unregistered_users = True
    poll.save()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)
    open_question = question_factory(poll=poll, is_open=True)

    assert Vote.objects.count() == 0

    url = reverse("polls-vote", kwargs={"pk": poll.pk})

    data = {
        "votes": {
            question.pk: {
                "choices": [choice1.pk],
                "other_choice_answer": "",
                "open_answer": "",
            },
            open_question.pk: {
                "choices": [],
                "other_choice_answer": "",
                "open_answer": "an open answer",
            },
        },
        "captcha": "testpass:0",
        "agreed_terms_of_use": True,
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1
    assert Answer.objects.count() == 1


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
@patch("adhocracy4.polls.api.reverse", return_value="/")
def test_agreement_update_with_vote(
    mock_provider,
    user,
    apiclient,
    poll_factory,
    question_factory,
    choice_factory,
    organisation_terms_of_use_factory,
):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    organisation_terms_of_use = organisation_terms_of_use_factory(
        user=user,
        organisation=poll.module.project.organisation,
        has_agreed=False,
    )
    assert not organisation_terms_of_use.has_agreed
    assert Vote.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse("polls-vote", kwargs={"pk": poll.pk})

    data = {
        "votes": {
            question.pk: {
                "choices": [choice1.pk],
                "other_choice_answer": "",
                "open_answer": "",
            },
        },
        "agreed_terms_of_use": True,
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1

    organisation_terms_of_use.refresh_from_db()
    assert organisation_terms_of_use.has_agreed


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
@patch("adhocracy4.polls.api.reverse", return_value="/")
def test_voting_without_agreement_forbidden(
    mock_provider, user, apiclient, poll_factory, question_factory, choice_factory
):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    apiclient.force_authenticate(user=user)

    url = reverse("polls-vote", kwargs={"pk": poll.pk})

    data = {
        "votes": {
            question.pk: {
                "choices": [choice1.pk],
                "other_choice_answer": "",
                "open_answer": "",
            },
        },
        "agreed_terms_of_use": False,
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
@patch("adhocracy4.polls.api.reverse", return_value="/")
def test_unregistered_user_voting_without_agreement_forbidden(
    mock_provider, user, apiclient, poll_factory, question_factory, choice_factory
):

    poll = poll_factory()
    poll.allow_unregistered_users = True
    poll.save()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    url = reverse("polls-vote", kwargs={"pk": poll.pk})

    data = {
        "votes": {
            question.pk: {
                "choices": [choice1.pk],
                "other_choice_answer": "",
                "open_answer": "",
            },
        },
        "agreed_terms_of_use": False,
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
@patch("adhocracy4.polls.api.reverse", return_value="/")
def test_voting_without_agreement_data_forbidden(
    mock_provider, user, apiclient, poll_factory, question_factory, choice_factory
):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    apiclient.force_authenticate(user=user)

    url = reverse("polls-vote", kwargs={"pk": poll.pk})

    data = {
        "votes": {
            question.pk: {
                "choices": [choice1.pk],
                "other_choice_answer": "",
                "open_answer": "",
            },
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
@patch("adhocracy4.polls.api.reverse", return_value="/")
def test_user_can_vote_with_already_agreed(
    mock_provider,
    user,
    apiclient,
    poll_factory,
    question_factory,
    choice_factory,
    organisation_terms_of_use_factory,
):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)
    open_question = question_factory(poll=poll, is_open=True)
    organisation_terms_of_use_factory(
        user=user,
        organisation=poll.project.organisation,
        has_agreed=True,
    )

    assert Vote.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse("polls-vote", kwargs={"pk": poll.pk})

    data = {
        "votes": {
            question.pk: {
                "choices": [choice1.pk],
                "other_choice_answer": "",
                "open_answer": "",
            },
            open_question.pk: {
                "choices": [],
                "other_choice_answer": "",
                "open_answer": "an open answer",
            },
        },
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1
    assert Answer.objects.count() == 1


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
@patch("adhocracy4.polls.api.reverse", return_value="/")
def test_agreement_saved_and_updated_with_other_choice_create_and_update(
    mock_provider, user, question, apiclient, choice_factory
):

    choice_factory(question=question)
    choice_other = choice_factory(question=question, is_other_choice=True)

    assert Vote.objects.count() == 0
    assert OtherVote.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse("polls-vote", kwargs={"pk": question.poll.pk})

    data = {
        "votes": {
            question.pk: {
                "choices": [choice_other.pk],
                "other_choice_answer": "other choice answer",
                "open_answer": "",
            }
        },
        "agreed_terms_of_use": True,
    }

    with active_phase(question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1
    assert OtherVote.objects.count() == 1
    assert OtherVote.objects.first().vote == Vote.objects.first()
    assert OtherVote.objects.first().answer == "other choice answer"

    terms = OrganisationTermsOfUse.objects.all()
    assert len(terms) == 1
    assert terms[0].user == user
    assert terms[0].has_agreed
    terms[0].has_agreed = False
    terms[0].save()

    data = {
        "votes": {
            question.pk: {
                "choices": [choice_other.pk],
                "other_choice_answer": "other choice answer updated",
                "open_answer": "",
            }
        },
        "agreed_terms_of_use": True,
    }

    with active_phase(question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1
    assert OtherVote.objects.count() == 1
    assert OtherVote.objects.first().vote == Vote.objects.first()
    assert OtherVote.objects.first().answer == "other choice answer updated"
    terms = OrganisationTermsOfUse.objects.all()
    assert len(terms) == 1
    assert terms[0].user == user
    assert terms[0].has_agreed


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
@patch("adhocracy4.polls.api.reverse", return_value="/")
def test_agreement_save_with_answer_create(
    mock_provider, user, open_question, apiclient
):

    assert Answer.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse("polls-vote", kwargs={"pk": open_question.poll.pk})

    data = {
        "votes": {
            open_question.pk: {
                "choices": [],
                "other_choice_answer": "",
                "open_answer": "answer to open question",
            }
        },
        "agreed_terms_of_use": True,
    }

    with active_phase(open_question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Answer.objects.count() == 1
    assert Answer.objects.first().answer == "answer to open question"
    terms = OrganisationTermsOfUse.objects.all()
    assert len(terms) == 1
    assert terms[0].user == user
    assert terms[0].has_agreed


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
@patch("adhocracy4.polls.api.reverse", return_value="/")
def test_agreement_saved_and_updated_with_answer_create_and_update(
    mock_provider, user, open_question, apiclient
):

    assert Answer.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse("polls-vote", kwargs={"pk": open_question.poll.pk})

    data = {
        "votes": {
            open_question.pk: {
                "choices": [],
                "other_choice_answer": "",
                "open_answer": "answer to open question",
            }
        },
        "agreed_terms_of_use": True,
    }

    with active_phase(open_question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Answer.objects.count() == 1
    assert Answer.objects.first().answer == "answer to open question"

    data = {
        "votes": {
            open_question.pk: {
                "choices": [],
                "other_choice_answer": "",
                "open_answer": "answer to open question updated",
            }
        },
        "agreed_terms_of_use": True,
    }

    with active_phase(open_question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Answer.objects.count() == 1
    assert Answer.objects.first().answer == "answer to open question updated"
    terms = OrganisationTermsOfUse.objects.all()
    assert len(terms) == 1
    assert terms[0].user == user
    assert terms[0].has_agreed


@pytest.mark.django_db
@patch("adhocracy4.polls.api.reverse", return_value="/")
def test_agreement_post_no_settings_no_effect(
    mock_provider, user, apiclient, poll_factory, question_factory, choice_factory
):
    """Sending in post without settings should not cause agreement create."""
    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)
    open_question = question_factory(poll=poll, is_open=True)

    assert Vote.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse("polls-vote", kwargs={"pk": poll.pk})

    data = {
        "votes": {
            question.pk: {
                "choices": [choice1.pk],
                "other_choice_answer": "",
                "open_answer": "",
            },
            open_question.pk: {
                "choices": [],
                "other_choice_answer": "",
                "open_answer": "an open answer",
            },
        },
        "agreed_terms_of_use": True,
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1
    assert Answer.objects.count() == 1
    terms = OrganisationTermsOfUse.objects.all()
    assert len(terms) == 0


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
@patch("adhocracy4.polls.api.reverse", return_value="/")
def test_agreement_info(
    mock_provider, admin, apiclient, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    assert Vote.objects.count() == 0

    apiclient.force_authenticate(user=admin)

    url = reverse("polls-vote", kwargs={"pk": poll.pk})

    data = {
        "votes": {
            question.pk: {
                "choices": [choice1.pk],
                "other_choice_answer": "",
                "open_answer": "",
            }
        },
        "agreed_terms_of_use": True,
    }

    response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Vote.objects.count() == 1
    terms = OrganisationTermsOfUse.objects.all()
    assert len(terms) == 1
    assert terms[0].user == admin


@pytest.mark.django_db
@override_settings(A4_USE_ORGANISATION_TERMS_OF_USE=True)
def test_agreement_without_terms_view_causes_error(
    admin, apiclient, poll_factory, question_factory, choice_factory
):
    """Accessing info without organisation-terms-of-use implemented fails."""
    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    assert Vote.objects.count() == 0

    apiclient.force_authenticate(user=admin)

    url = reverse("polls-vote", kwargs={"pk": poll.pk})

    data = {
        "votes": {
            question.pk: {
                "choices": [choice1.pk],
                "other_choice_answer": "",
                "open_answer": "",
            }
        },
        "agreed_terms_of_use": True,
    }

    with pytest.raises(NotImplementedError):
        apiclient.post(url, data, format="json")
