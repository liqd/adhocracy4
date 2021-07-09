import pytest
from django.urls import reverse
from rest_framework import status

from adhocracy4.polls.models import Answer
from adhocracy4.polls.models import OtherVote
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


@pytest.mark.django_db
def test_other_choice_vote_created(user,
                                   question,
                                   apiclient,
                                   choice_factory):

    choice_factory(question=question)
    choice_other = choice_factory(question=question, is_other_choice=True)

    assert Vote.objects.count() == 0
    assert OtherVote.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse(
        'votes-list',
        kwargs={
            'question_pk': question.pk
        })

    data = {
        'choices': [choice_other.pk],
        'other_choice_answer': 'other choice answer',
        'open_answer': ''
    }

    with active_phase(question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1
    assert OtherVote.objects.count() == 1
    assert OtherVote.objects.first().vote == Vote.objects.first()
    assert OtherVote.objects.first().answer == 'other choice answer'


@pytest.mark.django_db
def test_empty_other_choice_vote_raises_error(user,
                                              question,
                                              apiclient,
                                              choice_factory):

    choice_factory(question=question)
    choice_other = choice_factory(question=question, is_other_choice=True)

    assert Vote.objects.count() == 0
    assert OtherVote.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse(
        'votes-list',
        kwargs={
            'question_pk': question.pk
        })

    data = {
        'choices': [choice_other.pk],
        'other_choice_answer': '',
        'open_answer': ''
    }

    with active_phase(question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert Vote.objects.count() == 0
    assert OtherVote.objects.count() == 0


@pytest.mark.django_db
def test_other_choice_vote_updated(user,
                                   question,
                                   apiclient,
                                   choice_factory):

    choice_factory(question=question)
    choice_other = choice_factory(question=question, is_other_choice=True)

    assert Vote.objects.count() == 0
    assert OtherVote.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse(
        'votes-list',
        kwargs={
            'question_pk': question.pk
        })

    data = {
        'choices': [choice_other.pk],
        'other_choice_answer': 'other choice answer',
        'open_answer': ''
    }

    with active_phase(question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1
    assert OtherVote.objects.count() == 1
    assert OtherVote.objects.first().vote == Vote.objects.first()
    assert OtherVote.objects.first().answer == 'other choice answer'

    data = {
        'choices': [choice_other.pk],
        'other_choice_answer': 'other choice answer updated',
        'open_answer': ''
    }

    with active_phase(question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.count() == 1
    assert OtherVote.objects.count() == 1
    assert OtherVote.objects.first().vote == Vote.objects.first()
    assert OtherVote.objects.first().answer == 'other choice answer updated'


@pytest.mark.django_db
def test_answer_created(user,
                        open_question,
                        apiclient):

    assert Answer.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse(
        'votes-list',
        kwargs={
            'question_pk': open_question.pk
        })

    data = {
        'choices': [],
        'other_choice_answer': '',
        'open_answer': 'answer to open question'
    }

    with active_phase(open_question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    assert Answer.objects.count() == 1
    assert Answer.objects.first().answer == 'answer to open question'


@pytest.mark.django_db
def test_answer_updated(user,
                        open_question,
                        apiclient):

    assert Answer.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse(
        'votes-list',
        kwargs={
            'question_pk': open_question.pk
        })

    data = {
        'choices': [],
        'other_choice_answer': '',
        'open_answer': 'answer to open question'
    }

    with active_phase(open_question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    assert Answer.objects.count() == 1
    assert Answer.objects.first().answer == 'answer to open question'

    data = {
        'choices': [],
        'other_choice_answer': '',
        'open_answer': 'answer to open question updated'
    }

    with active_phase(open_question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    assert Answer.objects.count() == 1
    assert Answer.objects.first().answer == 'answer to open question updated'


@pytest.mark.django_db
def test_answer_deleted(user,
                        open_question,
                        apiclient):

    assert Answer.objects.count() == 0

    apiclient.force_authenticate(user=user)

    url = reverse(
        'votes-list',
        kwargs={
            'question_pk': open_question.pk
        })

    data = {
        'choices': [],
        'other_choice_answer': '',
        'open_answer': 'answer to open question'
    }

    with active_phase(open_question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    assert Answer.objects.count() == 1
    assert Answer.objects.first().answer == 'answer to open question'

    data = {
        'choices': [],
        'other_choice_answer': '',
        'open_answer': ''
    }

    with active_phase(open_question.poll.module, VotingPhase):
        response = apiclient.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    assert Answer.objects.count() == 0
