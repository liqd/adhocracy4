import pytest
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError

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
                           other_vote_factory,
                           question_factory,
                           choice_factory):

    poll = poll_factory()
    question1 = question_factory(poll=poll, label='question1')
    choice1_1 = choice_factory(question=question1)

    question2 = question_factory(poll=poll, multiple_choice=True,
                                 label='question2')
    choice2_1 = choice_factory(question=question2)
    choice2_2 = choice_factory(question=question2)
    choice2_3 = choice_factory(question=question2, is_other_choice=True)

    user1 = user_factory()
    user2 = user_factory()

    vote_factory(creator=user1, choice=choice1_1)
    vote_factory(creator=user1, choice=choice2_1)
    vote = vote_factory(creator=user1, choice=choice2_3)
    other_vote_factory(vote=vote)

    vote_factory(creator=user2, choice=choice2_1)
    vote_factory(creator=user2, choice=choice2_2)

    questions = Question.objects.annotate_vote_count()
    question1_annotated = questions.get(label='question1')
    question2_annotated = questions.get(label='question2')

    assert hasattr(question1_annotated, 'vote_count')
    assert hasattr(question2_annotated, 'vote_count_multi')
    assert question1_annotated.vote_count == 1
    assert question2_annotated.vote_count == 2
    assert question2_annotated.vote_count_multi == 4


@pytest.mark.django_db
def test_question_clean(poll_factory,
                        question_factory,
                        choice_factory):

    poll = poll_factory()
    question = question_factory(poll=poll)
    assert not question.multiple_choice
    assert not question.is_open
    assert not question.has_other_option

    question.is_open = True
    question.multiple_choice = True
    with pytest.raises(ValidationError):
        question.clean()

    question.multiple_choice = False
    question.clean()
    question.save()
    choice_factory(question=question, is_other_choice=True)
    with pytest.raises(ValidationError):
        question.clean()


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
def test_multi_choice_queryset(user_factory,
                               poll_factory,
                               vote_factory,
                               question_factory,
                               choice_factory):

    poll = poll_factory()
    question = question_factory(poll=poll, multiple_choice=True)
    choice1 = choice_factory(question=question)
    choice2 = choice_factory(question=question)

    user1 = user_factory()
    user2 = user_factory()

    vote_factory(creator=user1, choice=choice1)
    vote_factory(creator=user2, choice=choice1)
    vote_factory(creator=user2, choice=choice2)

    choices = Choice.objects.annotate_vote_count()

    assert hasattr(choices.first(), 'vote_count')
    assert choices.first().vote_count == 2
    assert choices.last().vote_count == 1


@pytest.mark.django_db
def test_get_absolute_url(poll, vote, question, answer,
                          choice, other_vote):

    assert poll.get_absolute_url() == \
        poll.project.get_absolute_url()
    assert question.get_absolute_url() == \
        question.poll.get_absolute_url()
    assert answer.get_absolute_url() == \
        answer.question.poll.get_absolute_url()
    assert choice.get_absolute_url() == \
        choice.question.poll.get_absolute_url()
    assert vote.get_absolute_url() == \
        vote.choice.question.poll.get_absolute_url()
    assert other_vote.get_absolute_url() == \
        other_vote.vote.choice.question.poll.get_absolute_url()

    assert str(answer) == '%s: %s' % (answer.creator, answer.answer[:20])

    assert str(vote) == '%s: %s' % (vote.creator, vote.choice)
    assert vote.module == vote.choice.question.poll.module
    assert vote.project == vote.module.project

    assert str(other_vote) == '%s: %s' % (other_vote.vote.creator, 'other')
    assert other_vote.module == other_vote.vote.choice.question.poll.module
    assert other_vote.project == other_vote.module.project
