import base64
from io import BytesIO

import pytest
from django.core.files.base import ContentFile
from django.urls import reverse
from PIL import Image
from rest_framework import status

from adhocracy4.polls.models import Question
from adhocracy4.polls.phases import VotingPhase
from tests.helpers import active_phase


def _base64_image():
    img = Image.new("RGB", (1500, 500), color="red")
    buf = BytesIO()
    img.save(buf, format="JPEG")
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


@pytest.mark.django_db
def test_anonymous_user_can_not_update_poll(
    apiclient, poll_factory, question_factory, choice_factory
):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice_factory(question=question)
    choice_factory(question=question)

    url = reverse("polls-detail", kwargs={"pk": poll.pk})

    response = apiclient.patch(url, {}, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_anonymous_user_cannot_update_poll_if_allowed(
    apiclient, poll_factory, question_factory, choice_factory
):

    poll = poll_factory()
    poll.allow_unregistered_users = True
    poll.save()
    question = question_factory(poll=poll)
    choice_factory(question=question)
    choice_factory(question=question)

    url = reverse("polls-detail", kwargs={"pk": poll.pk})

    response = apiclient.patch(url, {}, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_can_not_update_poll(
    apiclient, user, poll_factory, question_factory, choice_factory
):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice_factory(question=question)
    choice_factory(question=question)

    url = reverse("polls-detail", kwargs={"pk": poll.pk})

    apiclient.force_authenticate(user=user)

    response = apiclient.post(url, {}, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_normal_user_cannot_change_poll_in_active_phase(
    user, apiclient, poll_factory, question_factory
):

    poll = poll_factory()
    question_factory(poll=poll)

    apiclient.force_authenticate(user=user)

    url = reverse("polls-detail", kwargs={"pk": poll.pk})

    data = {}

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_can_update_poll(
    apiclient, admin, poll_factory, question_factory, choice_factory
):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice2 = choice_factory(question=question)

    assert Question.objects.count() == 1

    url = reverse("polls-detail", kwargs={"pk": poll.pk})

    apiclient.force_authenticate(user=admin)

    data = {
        "questions": [
            {
                "id": question.id,
                "label": "bla",
                "help_text": "blubb",
                "multiple_choice": True,
                "is_open": False,
                "choices": [
                    {
                        "id": choice1.pk,
                        "label": "choice1",
                        "is_other_choice": False,
                        "count": 1,
                    },
                    {
                        "id": choice2.pk,
                        "label": "choice2",
                        "is_other_choice": False,
                        "count": 2,
                    },
                ],
                "answers": [],
            },
            {
                "label": "bla",
                "help_text": "blubb",
                "multiple_choice": False,
                "is_open": False,
                "choices": [
                    {"label": "choice1", "is_other_choice": False, "count": 1},
                    {"label": "choice2", "is_other_choice": True, "count": 2},
                ],
                "answers": [],
            },
        ]
    }

    response = apiclient.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert Question.objects.count() == 2
    assert Question.objects.last().has_other_option

    data = {
        "questions": [
            {
                "id": question.id,
                "label": "bla",
                "help_text": "blubb",
                "multiple_choice": True,
                "is_open": False,
                "choices": [
                    {
                        "id": choice1.pk,
                        "label": "choice1",
                        "is_other_choice": False,
                        "count": 1,
                    },
                    {
                        "id": choice2.pk,
                        "label": "choice2",
                        "is_other_choice": False,
                        "count": 2,
                    },
                ],
                "answers": [],
            }
        ]
    }

    response = apiclient.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert Question.objects.count() == 1

    data = {
        "questions": [
            {
                "id": question.id,
                "label": "bla",
                "help_text": "blubb",
                "multiple_choice": True,
                "is_open": False,
                "choices": [
                    {
                        "id": choice1.pk,
                        "label": "choice1",
                        "is_other_choice": False,
                        "count": 1,
                    },
                    {
                        "id": choice2.pk,
                        "label": "choice2",
                        "is_other_choice": False,
                        "count": 2,
                    },
                ],
                "answers": [],
            },
            {
                "label": "open question",
                "help_text": "blubb",
                "multiple_choice": False,
                "is_open": True,
                "choices": [],
                "answers": [],
            },
        ]
    }

    response = apiclient.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert Question.objects.count() == 2
    assert Question.objects.filter(is_open=True).count() == 1


@pytest.mark.django_db
def test_user_choices_included_in_response(
    apiclient, user, poll_factory, question_factory, choice_factory, vote_factory
):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice2 = choice_factory(question=question)
    vote_factory(creator=user, choice=choice1)

    assert Question.objects.count() == 1

    url = reverse("polls-detail", kwargs={"pk": poll.pk})

    apiclient.force_authenticate(user=user)
    response = apiclient.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["questions"][0]["userChoices"][0] == choice1.pk
    assert choice2.pk not in response.data["questions"][0]["userChoices"]


@pytest.mark.django_db
def test_user_answers_included_in_response(
    apiclient, user, poll_factory, open_question_factory, answer_factory
):

    poll = poll_factory()
    question = open_question_factory(poll=poll)
    answer = answer_factory(creator=user, answer="user answer", question=question)

    assert Question.objects.count() == 1

    url = reverse("polls-detail", kwargs={"pk": poll.pk})

    apiclient.force_authenticate(user=user)
    response = apiclient.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["questions"][0]["userAnswer"] == answer.id


@pytest.mark.django_db
def test_question_image_requires_alt_text(
    apiclient, admin, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    question = question_factory(poll=poll)
    choice_factory(question=question)
    choice_factory(question=question)

    url = reverse("polls-detail", kwargs={"pk": poll.pk})
    apiclient.force_authenticate(user=admin)

    b64_image = _base64_image()

    data = {
        "questions": [
            {
                "id": question.id,
                "label": "question with image",
                "help_text": "",
                "multiple_choice": False,
                "is_open": False,
                "choices": [
                    {"label": "a", "is_other_choice": False, "count": 0},
                    {"label": "b", "is_other_choice": False, "count": 0},
                ],
                "answers": [],
                "image_base64": b64_image,
                "image_alt_text": "",
            }
        ]
    }

    response = apiclient.put(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "image_alt_text" in str(response.content)


@pytest.mark.django_db
def test_question_image_with_alt_text_succeeds(
    apiclient, admin, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    question = question_factory(poll=poll)
    choice_factory(question=question)
    choice_factory(question=question)

    url = reverse("polls-detail", kwargs={"pk": poll.pk})
    apiclient.force_authenticate(user=admin)

    b64_image = _base64_image()

    data = {
        "questions": [
            {
                "id": question.id,
                "label": "question with image and alt text",
                "help_text": "",
                "multiple_choice": False,
                "is_open": False,
                "choices": [
                    {"label": "a", "is_other_choice": False, "count": 0},
                    {"label": "b", "is_other_choice": False, "count": 0},
                ],
                "answers": [],
                "image_base64": b64_image,
                "image_alt_text": "A red rectangle",
            }
        ]
    }

    response = apiclient.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    question.refresh_from_db()
    assert question.image
    assert question.image_alt_text == "A red rectangle"


@pytest.mark.django_db
def test_question_existing_image_requires_alt_text(
    apiclient, admin, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    question = question_factory(poll=poll)
    choice_factory(question=question)
    choice_factory(question=question)

    b64_image = _base64_image()

    question.image.save(
        "test.jpg",
        ContentFile(base64.b64decode(b64_image.split(";base64,")[1])),
    )
    question.image_alt_text = ""
    question.save()

    url = reverse("polls-detail", kwargs={"pk": poll.pk})
    apiclient.force_authenticate(user=admin)

    data = {
        "questions": [
            {
                "id": question.id,
                "label": "updated label",
                "help_text": "",
                "multiple_choice": False,
                "is_open": False,
                "choices": [
                    {"label": "a", "is_other_choice": False, "count": 0},
                    {"label": "b", "is_other_choice": False, "count": 0},
                ],
                "answers": [],
                "image_alt_text": "",
            }
        ]
    }

    response = apiclient.put(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_question_existing_image_with_alt_text_succeeds(
    apiclient, admin, poll_factory, question_factory, choice_factory
):
    poll = poll_factory()
    question = question_factory(poll=poll)
    choice_factory(question=question)
    choice_factory(question=question)

    b64_image = _base64_image()

    question.image.save(
        "test.jpg",
        ContentFile(base64.b64decode(b64_image.split(";base64,")[1])),
    )
    question.image_alt_text = ""
    question.save()

    url = reverse("polls-detail", kwargs={"pk": poll.pk})
    apiclient.force_authenticate(user=admin)

    data = {
        "questions": [
            {
                "id": question.id,
                "label": "updated label with alt text",
                "help_text": "",
                "multiple_choice": False,
                "is_open": False,
                "choices": [
                    {"label": "a", "is_other_choice": False, "count": 0},
                    {"label": "b", "is_other_choice": False, "count": 0},
                ],
                "answers": [],
                "image_alt_text": "A red rectangle with description",
            }
        ]
    }

    response = apiclient.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    question.refresh_from_db()
    assert question.image_alt_text == "A red rectangle with description"
