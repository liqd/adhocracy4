import pytest
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError

from adhocracy4.polls.models import Choice
from adhocracy4.polls.models import Question


@pytest.mark.django_db
def test_question_choice_list(user,
                              question,
                              vote_factory,
                              choice_factory):

    choice1 = choice_factory(question=question)
    choice_factory(question=question)

    anonym = AnonymousUser()
    assert question.user_choices_list(anonym) == []

    vote_factory(creator=user, choice=choice1)

    assert len(question.user_choices_list(user)) == 1
    assert question.user_choices_list(user)[0] == choice1.id


@pytest.mark.django_db
def test_user_answer(open_question,
                     user_factory,
                     answer_factory):

    user1 = user_factory()
    user2 = user_factory()
    anonymous = AnonymousUser()

    answer = answer_factory(creator=user1, answer='user answer',
                            question=open_question)
    assert open_question.user_answer(anonymous) == ''
    assert open_question.user_answer(user1) == answer.id
    assert open_question.user_answer(user2) == ''


@pytest.mark.django_db
def test_question_queryset(poll,
                           user_factory,
                           vote_factory,
                           other_vote_factory,
                           question_factory,
                           open_question_factory,
                           choice_factory,
                           other_choice_factory,
                           answer_factory):

    question1 = question_factory(poll=poll, label='question1')
    choice1_1 = choice_factory(question=question1)

    question2 = question_factory(poll=poll, multiple_choice=True,
                                 label='question2')
    choice2_1 = choice_factory(question=question2)
    choice2_2 = choice_factory(question=question2)
    choice2_3 = other_choice_factory(question=question2)

    question3 = open_question_factory(poll=poll, label='question3')

    user1 = user_factory()
    user2 = user_factory()

    vote_factory(creator=user1, choice=choice1_1)
    vote_factory(creator=user1, choice=choice2_1)
    vote = vote_factory(creator=user1, choice=choice2_3)
    other_vote_factory(vote=vote)
    answer_factory(creator=user1, answer='bla', question=question3)

    vote_factory(creator=user2, choice=choice2_1)
    vote_factory(creator=user2, choice=choice2_2)

    questions = Question.objects.annotate_vote_count()
    question1_annotated = questions.get(label='question1')
    question2_annotated = questions.get(label='question2')
    question3_annotated = questions.get(label='question3')

    assert hasattr(question1_annotated, 'vote_count')
    assert hasattr(question2_annotated, 'vote_count_multi')
    assert hasattr(question3_annotated, 'answer_count')

    assert question1_annotated.vote_count == 1
    assert question1_annotated.vote_count == 1
    assert question1_annotated.answer_count == 0

    assert question2_annotated.vote_count == 2
    assert question2_annotated.vote_count_multi == 4
    assert question2_annotated.answer_count == 0

    assert question3_annotated.vote_count == 0
    assert question3_annotated.vote_count_multi == 0
    assert question3_annotated.answer_count == 1


@pytest.mark.django_db
def test_question_clean(question,
                        choice_factory):

    assert not question.multiple_choice
    assert not question.is_open
    assert not question.has_other_option

    choice_factory(question=question)
    question.is_open = True
    with pytest.raises(ValidationError) as error:
        question.save()
    assert error.value.messages[0].\
        startswith('Question with choices cannot become open question.')

    question.choices.all().delete()
    question.is_open = True
    question.save()

    question.multiple_choice = True
    with pytest.raises(ValidationError) as error:
        question.save()
    assert error.value.messages[0] == \
           'Questions with open answers cannot have multiple choices.'


@pytest.mark.django_db
def test_answer_clean(question,
                      open_question,
                      answer_factory):

    with pytest.raises(ValidationError) as error:
        answer_factory(question=question)
    assert error.value.messages[0] == \
           'Only open questions can have answers.'

    answer_factory(question=open_question)


@pytest.mark.django_db
def test_choice_queryset(question,
                         user_factory,
                         vote_factory,
                         choice_factory):

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
def test_choice_clean(question,
                      choice_factory):

    with pytest.raises(ValidationError) as error:
        choice_factory(question=question, is_other_choice=True)
    assert error.value.messages[0].\
        startswith('"Other" cannot be the only choice.')

    question.is_open = True
    question.save()
    with pytest.raises(ValidationError) as error:
        choice_factory(question=question, is_other_choice=True)
    assert error.value.messages[0].\
        startswith('Open questions cannot have choices.')


@pytest.mark.django_db
def test_multi_choice_queryset(question,
                               user_factory,
                               vote_factory,
                               choice_factory):

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
def test_other_vote_clean(vote,
                          vote_on_other,
                          other_vote_factory):

    with pytest.raises(ValidationError) as error:
        other_vote_factory(vote=vote)
    assert error.value.messages[0] == \
           'Other vote can only be created for vote on "other" choice.'

    other_vote_factory(vote=vote_on_other)
    assert vote_on_other.is_other_vote


@pytest.mark.django_db
def test_get_absolute_url(poll, question, vote, answer,
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
