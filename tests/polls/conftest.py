from pytest_factoryboy import register

from meinberlin.apps.test.factories import polls

register(polls.PollFactory)
register(polls.QuestionFactory)
register(polls.ChoiceFactory)
register(polls.VoteFactory)
