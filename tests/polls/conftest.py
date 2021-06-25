import pytest
from pytest_factoryboy import register

from tests.polls import factories as poll_factories

register(poll_factories.PollFactory)
register(poll_factories.QuestionFactory)
register(poll_factories.OpenQuestionFactory, 'open_question')
register(poll_factories.AnswerFactory)
register(poll_factories.ChoiceFactory)
register(poll_factories.OtherChoiceFactory, 'other_choice')
register(poll_factories.VoteFactory)
register(poll_factories.VoteOnOtherChoiceFactory, 'vote_on_other')
register(poll_factories.OtherVoteFactory)


@pytest.fixture
def answer__question(open_question):
    return open_question


@pytest.fixture
def other_vote__vote(vote_on_other):
    return vote_on_other


@pytest.fixture
def vote_on_other__choice(other_choice):
    return other_choice
