import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse

from adhocracy4.polls.models import Poll
from adhocracy4.polls.validators import single_item_per_module
from adhocracy4.polls.validators import single_vote_per_user


@pytest.mark.django_db
def test_choice_belongs_to_question(admin,
                                    apiclient,
                                    poll_factory,
                                    question_factory,
                                    choice_factory):

    poll = poll_factory()
    question1 = question_factory(poll=poll)
    choice_factory(question=question1)
    question2 = question_factory(poll=poll)
    choice2 = choice_factory(question=question2)

    apiclient.force_authenticate(user=admin)

    url = reverse(
        'votes-list',
        kwargs={
            'question_pk': question1.pk
        })

    data = {
        'choices': [choice2.pk],
        'other_choice_answer': '',
        'open_answer': ''
    }

    with pytest.raises(ValidationError):
        apiclient.post(url, data, format='json')


@pytest.mark.django_db
def test_single_vote_per_user(admin,
                              apiclient,
                              poll_factory,
                              vote_factory,
                              question_factory,
                              choice_factory):

    poll = poll_factory()
    question1 = question_factory(poll=poll, multiple_choice=False)
    choice1 = choice_factory(question=question1)

    vote_factory(creator=admin, choice=choice1)

    with pytest.raises(ValidationError):
        single_vote_per_user(admin, choice1)


@pytest.mark.django_db
def test_single_item_per_module(poll_factory):

    poll = poll_factory()
    module = poll.module

    with pytest.raises(ValidationError):
        single_item_per_module(module, Poll)
