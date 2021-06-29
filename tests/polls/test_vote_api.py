import pytest
from django.urls import reverse
from rest_framework import status

from adhocracy4.polls.models import Vote
from adhocracy4.polls.phases import VotingPhase
from adhocracy4.projects.enums import Access
from tests.helpers import active_phase


@pytest.mark.django_db
def test_anonymous_user_can_not_vote(apiclient,
                                     poll_factory,
                                     question_factory,
                                     choice_factory):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    assert Vote.objects.count() == 0

    url = reverse(
        'votes-list',
        kwargs={
            'question_pk': question.pk
        })

    data = {
        'choices': [choice1.pk],
        'other_choice_answer': '',
        'open_answer': ''
    }

    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert Vote.objects.count() == 0


@pytest.mark.django_db
def test_normal_user_can_not_vote(user,
                                  apiclient,
                                  poll_factory,
                                  question_factory,
                                  choice_factory):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    assert Vote.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse(
        'votes-list',
        kwargs={
            'question_pk': question.pk
        })

    data = {
        'choices': [choice1.pk],
        'other_choice_answer': '',
        'open_answer': ''
    }

    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert Vote.objects.count() == 0


@pytest.mark.django_db
def test_admin_can_vote(admin,
                        apiclient,
                        poll_factory,
                        question_factory,
                        choice_factory):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    assert Vote.objects.count() == 0

    apiclient.force_authenticate(user=admin)

    url = reverse(
        'votes-list',
        kwargs={
            'question_pk': question.pk
        })

    data = {
        'choices': [choice1.pk],
        'other_choice_answer': '',
        'open_answer': ''
    }

    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1


@pytest.mark.django_db
def test_normal_user_can_vote_in_active_phase(user,
                                              apiclient,
                                              poll_factory,
                                              question_factory,
                                              choice_factory):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    assert Vote.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse(
        'votes-list',
        kwargs={
            'question_pk': question.pk
        })

    data = {
        'choices': [choice1.pk],
        'other_choice_answer': '',
        'open_answer': ''
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1


@pytest.mark.django_db
def test_user_cant_vote_in_private_project(user,
                                           apiclient,
                                           poll_factory,
                                           question_factory,
                                           choice_factory):

    poll = poll_factory()
    project = poll.module.project
    project.access = Access.PRIVATE
    project.save()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    assert Vote.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse(
        'votes-list',
        kwargs={
            'question_pk': question.pk
        })

    data = {
        'choices': [choice1.pk],
        'other_choice_answer': '',
        'open_answer': ''
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    assert Vote.objects.count() == 0


@pytest.mark.django_db
def test_participant_can_vote_in_private_project(user,
                                                 apiclient,
                                                 poll_factory,
                                                 question_factory,
                                                 choice_factory):

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

    url = reverse(
        'votes-list',
        kwargs={
            'question_pk': question.pk
        })

    data = {
        'choices': [choice1.pk],
        'other_choice_answer': '',
        'open_answer': ''
    }

    with active_phase(poll.module, VotingPhase):
        response = apiclient.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1
