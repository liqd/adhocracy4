import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status

from adhocracy4.polls.models import Poll
from adhocracy4.polls.validators import single_item_per_module


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
