import base64
import io

import pytest
from django.core.exceptions import ValidationError
from django.test import override_settings
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.exceptions import ValidationError as RestValidationError

from adhocracy4.polls.models import Poll
from adhocracy4.polls.validators import single_item_per_module
from adhocracy4.polls.validators import validate_poll_question_image


def _encoded_image(width, height):
    buffer = io.BytesIO()
    Image.new("RGB", (width, height)).save(buffer, "PNG")
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()


@override_settings(IMAGE_ALIASES={"questionimage": {"min_resolution": (100, 100)}})
def test_poll_question_image_uses_configured_min_resolution():
    # the stated minimum is accepted ...
    validate_poll_question_image(_encoded_image(100, 100))
    # ... and a couple of pixels below it are tolerated (rounding)
    validate_poll_question_image(_encoded_image(98, 98))

    with pytest.raises(RestValidationError):
        validate_poll_question_image(_encoded_image(97, 100))

    with pytest.raises(RestValidationError):
        validate_poll_question_image(_encoded_image(100, 97))


@pytest.mark.django_db
def test_choice_belongs_to_question(
    admin, apiclient, poll_factory, question_factory, choice_factory
):

    poll = poll_factory()
    question1 = question_factory(poll=poll)
    choice_factory(question=question1)
    question2 = question_factory(poll=poll)
    choice2 = choice_factory(question=question2)

    apiclient.force_authenticate(user=admin)

    url = reverse("polls-vote", kwargs={"pk": question1.poll.pk})

    data = {
        "votes": {
            question1.pk: {
                "choices": [choice2.pk],
                "other_choice_answer": "",
                "open_answer": "",
            }
        }
    }
    response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_single_item_per_module(poll_factory):

    poll = poll_factory()
    module = poll.module

    with pytest.raises(ValidationError):
        single_item_per_module(module, Poll)
