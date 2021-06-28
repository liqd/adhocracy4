import pytest
from django.urls import reverse
from rest_framework import status

from adhocracy4.polls.models import Question


@pytest.mark.django_db
def test_anonymous_user_can_not_update_poll(apiclient,
                                            poll_factory,
                                            question_factory,
                                            choice_factory):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice_factory(question=question)
    choice_factory(question=question)

    url = reverse(
        'polls-detail',
        kwargs={
            'pk': poll.pk
        })

    response = apiclient.patch(url, {}, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_can_update_poll(apiclient,
                               admin,
                               poll_factory,
                               question_factory,
                               choice_factory):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice2 = choice_factory(question=question)

    assert Question.objects.count() == 1

    url = reverse(
        'polls-detail',
        kwargs={
            'pk': poll.pk
        })

    apiclient.force_authenticate(user=admin)

    data = {
        'questions': [
            {
                'id': question.id,
                'label': 'bla',
                'help_text': 'blubb',
                'multiple_choice': True,
                'is_open': False,
                'choices': [
                    {
                        'id': choice1.pk,
                        'label': 'choice1',
                        'is_other_choice': False,
                        'count': 1,
                    },
                    {
                        'id': choice2.pk,
                        'label': 'choice2',
                        'is_other_choice': False,
                        'count': 2,
                    },
                ],
                'answers': [],
            },
            {
                'label': 'bla',
                'help_text': 'blubb',
                'multiple_choice': False,
                'is_open': False,
                'choices': [
                    {
                        'label': 'choice1',
                        'is_other_choice': False,
                        'count': 1
                    },
                    {
                        'label': 'choice2',
                        'is_other_choice': False,
                        'count': 2
                    },
                ],
                'answers': [],
            }
        ]
    }

    response = apiclient.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert Question.objects.count() == 2

    data = {
        'questions': [
            {
                'id': question.id,
                'label': 'bla',
                'help_text': 'blubb',
                'multiple_choice': True,
                'is_open': False,
                'choices': [
                    {
                        'id': choice1.pk,
                        'label': 'choice1',
                        'is_other_choice': False,
                        'count': 1
                    },
                    {
                        'id': choice2.pk,
                        'label': 'choice2',
                        'is_other_choice': False,
                        'count': 2
                    },
                ],
                'answers': [],
            }
        ]
    }

    response = apiclient.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert Question.objects.count() == 1
