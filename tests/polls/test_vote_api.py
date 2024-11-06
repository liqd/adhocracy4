from unittest.mock import MagicMock

import pytest
from django.urls import reverse
from rest_framework import status

from adhocracy4.polls.api import PollViewSet
from adhocracy4.polls.models import Answer
from adhocracy4.polls.models import OtherVote
from adhocracy4.polls.models import Vote
from adhocracy4.polls.phases import VotingPhase
from adhocracy4.polls.signals import poll_voted
from adhocracy4.projects.enums import Access
from tests.helpers import active_phase


@pytest.mark.django_db
def test_anonymous_user_can_not_vote(
    apiclient, poll_factory, question_factory, choice_factory
):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    assert Vote.objects.count() == 0

    url = reverse("polls-vote", kwargs={"pk": poll.pk})

    data = {
        "votes": {
            question.pk: {
                "choices": [choice1.pk],
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }

    response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert Vote.objects.count() == 0


@pytest.mark.django_db
def test_normal_user_can_not_vote(
    user, apiclient, poll_factory, question_factory, choice_factory
):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    assert Vote.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse("polls-vote", kwargs={"pk": poll.pk})

    data = {
        "votes": {
            question.pk: {
                "choices": [choice1.pk],
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }

    response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert Vote.objects.count() == 0


@pytest.mark.django_db
def test_admin_can_vote(
    admin, apiclient, poll_factory, question_factory, choice_factory
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
        }
    }

    response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1


@pytest.mark.django_db
def test_normal_user_can_vote_in_active_phase(
    user, apiclient, poll_factory, question_factory, choice_factory
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
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1
    assert Answer.objects.count() == 1


@pytest.mark.django_db
def test_anonymous_user_cannot_vote_in_active_phase_wrong_captcha(
    apiclient, poll_factory, question_factory, choice_factory
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
        "captcha": "",
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    data["captcha"] = "wrongcaptcha"
    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_anonymous_user_can_vote_in_active_phase_which_allows_unregistered_users(
    apiclient, poll_factory, question_factory, choice_factory
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
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1
    assert Answer.objects.count() == 1
    assert len(Vote.objects.first().content_id.hex) == 32
    assert len(Answer.objects.first().content_id.hex) == 32


@pytest.mark.django_db
def test_user_cant_vote_in_private_project(
    user, apiclient, poll_factory, question_factory, choice_factory
):

    poll = poll_factory()
    project = poll.module.project
    project.access = Access.PRIVATE
    project.save()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    assert Vote.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse("polls-vote", kwargs={"pk": poll.pk})

    data = {
        "votes": {
            question.pk: {
                "choices": [choice1.pk],
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    assert Vote.objects.count() == 0


@pytest.mark.django_db
def test_unregistered_user_cant_vote_in_private_project_with_allow_unregistered_users(
    apiclient, poll_factory, question_factory, choice_factory
):

    poll = poll_factory()
    poll.allow_unregistered_users = True
    poll.save()
    project = poll.module.project
    project.access = Access.PRIVATE
    project.save()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    assert Vote.objects.count() == 0

    url = reverse("polls-vote", kwargs={"pk": poll.pk})

    data = {
        "votes": {
            question.pk: {
                "choices": [choice1.pk],
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    assert Vote.objects.count() == 0


@pytest.mark.django_db
def test_participant_can_vote_in_private_project(
    user, apiclient, poll_factory, question_factory, choice_factory
):

    poll = poll_factory()
    project = poll.module.project
    project.access = Access.PRIVATE
    project.participants.add(user)
    project.save()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    assert Vote.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse("polls-vote", kwargs={"pk": poll.pk})

    data = {
        "votes": {
            question.pk: {
                "choices": [choice1.pk],
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1


@pytest.mark.django_db
def test_other_choice_vote_created(user, question, apiclient, choice_factory):

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
        }
    }

    with active_phase(question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1
    assert OtherVote.objects.count() == 1
    assert OtherVote.objects.first().vote == Vote.objects.first()
    assert OtherVote.objects.first().answer == "other choice answer"


@pytest.mark.django_db
def test_empty_other_choice_vote_raises_error(
    user, question, apiclient, choice_factory
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
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }

    with active_phase(question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert Vote.objects.count() == 0
    assert OtherVote.objects.count() == 0


@pytest.mark.django_db
def test_other_choice_vote_updated(user, question, apiclient, choice_factory):

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
        }
    }

    with active_phase(question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1
    assert OtherVote.objects.count() == 1
    assert OtherVote.objects.first().vote == Vote.objects.first()
    assert OtherVote.objects.first().answer == "other choice answer"

    data = {
        "votes": {
            question.pk: {
                "choices": [choice_other.pk],
                "other_choice_answer": "other choice answer updated",
                "open_answer": "",
            }
        }
    }

    with active_phase(question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1
    assert OtherVote.objects.count() == 1
    assert OtherVote.objects.first().vote == Vote.objects.first()
    assert OtherVote.objects.first().answer == "other choice answer updated"


@pytest.mark.django_db
def test_answer_created(user, open_question, apiclient):

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
        }
    }

    with active_phase(open_question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Answer.objects.count() == 1
    assert Answer.objects.first().answer == "answer to open question"


@pytest.mark.django_db
def test_answer_updated(user, open_question, apiclient):

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
        }
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
        }
    }

    with active_phase(open_question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Answer.objects.count() == 1
    assert Answer.objects.first().answer == "answer to open question updated"


@pytest.mark.django_db
def test_answer_deleted(user, open_question, apiclient):

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
        }
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
                "open_answer": "",
            }
        }
    }

    with active_phase(open_question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    assert Answer.objects.count() == 0


@pytest.mark.django_db
def test_get_data(apiclient, user, question, choice_factory):

    assert question.choices.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse("polls-vote", kwargs={"pk": question.poll.pk})

    data = {
        "votes": {
            question.pk: {"choices": [1], "other_choice_answer": "", "open_answer": ""}
        }
    }

    with active_phase(question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    choice = choice_factory(question=question)
    data = {
        "votes": {
            question.pk: {
                "choices": [choice.id],
                "other_choice_answer": "",
            }
        }
    }

    with active_phase(question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_validate_choices(apiclient, user, question_factory, choice_factory):

    question1 = question_factory()
    choice1 = choice_factory(question=question1)

    apiclient.force_authenticate(user=user)

    url = reverse("polls-vote", kwargs={"pk": question1.poll.pk})

    data = {
        "votes": {
            question1.pk: {
                "choices": [choice1.id, choice1.id],
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }

    with active_phase(question1.poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Duplicate choices detected" in response.content.decode()

    choice2 = choice_factory(question=question1)

    data = {
        "votes": {
            question1.pk: {
                "choices": [choice1.id, choice2.id],
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }
    with active_phase(question1.poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Multiple choice disabled for question" in response.content.decode()

    question2 = question_factory()

    url = reverse("polls-vote", kwargs={"pk": question2.poll.pk})

    data = {
        "votes": {
            question2.pk: {
                "choices": [choice1.id],
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }

    with active_phase(question2.poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        "Choice has to belong to the question set in the url."
        in response.content.decode()
    )


@pytest.mark.django_db
def test_validate_question_belongs_to_poll(
    apiclient, user, poll_factory, question_factory, choice_factory
):

    poll_1 = poll_factory()
    poll_2 = poll_factory()
    question1 = question_factory(poll=poll_1)
    choice1 = choice_factory(question=question1)

    apiclient.force_authenticate(user=user)

    url = reverse("polls-vote", kwargs={"pk": poll_2.pk})

    data = {
        "votes": {
            question1.pk: {
                "choices": [choice1.id],
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }

    with active_phase(poll_2.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        "Question has to belong to the poll set in the url."
        in response.content.decode()
    )


@pytest.mark.django_db
def test_poll_voted_signal_is_dispatched_on_vote(
    user, apiclient, poll_factory, question_factory, choice_factory
):
    signal_handler = MagicMock()
    poll_voted.connect(signal_handler)

    poll = poll_factory()
    poll.allow_unregistered_users = True
    poll.save()
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
        }
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        signal_handler.assert_called_once_with(
            signal=poll_voted,
            sender=PollViewSet,
            poll=poll,
            creator=user,
            content_id=None,
        )
        assert Vote.objects.count() == 1

        # test for unregistered user
        signal_handler.reset_mock()
        apiclient.logout()
        data["captcha"] = "testpass:0"
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Vote.objects.count() == 2
        content_id = Vote.objects.filter(content_id__isnull=False).first().content_id
        signal_handler.assert_called_once_with(
            signal=poll_voted,
            sender=PollViewSet,
            poll=poll,
            creator=None,
            content_id=content_id,
        )
