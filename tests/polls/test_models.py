import pytest
from django.contrib.auth.models import AnonymousUser

from adhocracy4.polls.models import Choice
from adhocracy4.polls.models import Question


@pytest.mark.django_db
def test_question_choice_list(user,
                              poll_factory,
                              vote_factory,
                              question_factory,
                              choice_factory):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    anonym = AnonymousUser()

    assert question.user_choices_list(anonym) == []

    vote_factory(creator=user, choice=choice1)

    assert len(question.user_choices_list(user)) == 1
    assert question.user_choices_list(user)[0] == choice1.id


@pytest.mark.django_db
def test_question_queryset(user_factory,
                           poll_factory,
                           vote_factory,
                           question_factory,
                           choice_factory):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice2 = choice_factory(question=question)

    user1 = user_factory()
    user2 = user_factory()

    vote_factory(creator=user1, choice=choice1)
    vote_factory(creator=user2, choice=choice2)

    questions = Question.objects.annotate_vote_count()

    assert hasattr(questions.first(), 'vote_count')
    assert questions.first().vote_count == 2


@pytest.mark.django_db
def test_choice_queryset(user_factory,
                         poll_factory,
                         vote_factory,
                         question_factory,
                         choice_factory):

    poll = poll_factory()
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)
    choice2 = choice_factory(question=question)

    user1 = user_factory()
    user2 = user_factory()

    vote_factory(creator=user1, choice=choice1)
    vote_factory(creator=user2, choice=choice2)

    choices = Choice.objects.annotate_vote_count()

    assert hasattr(choices.first(), 'vote_count')
    assert choices.first().vote_count == 1


@pytest.mark.django_db
def test_get_absolute_url(poll, vote, question, choice):

    assert poll.get_absolute_url() == \
        poll.project.get_absolute_url()
    assert choice.get_absolute_url() == \
        choice.question.poll.get_absolute_url()
    assert vote.get_absolute_url() == \
        vote.choice.question.poll.get_absolute_url()

    assert str(vote) == '%s: %s' % (vote.creator, vote.choice)
    assert vote.module == vote.choice.question.poll.module
    assert vote.project == vote.module.project
