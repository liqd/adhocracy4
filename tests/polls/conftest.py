from pytest_factoryboy import register

from adhocracy4.test.factories import polls

register(polls.PollFactory)
register(polls.QuestionFactory)
register(polls.ChoiceFactory)
register(polls.VoteFactory)
