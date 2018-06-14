from pytest_factoryboy import register

from tests.polls import factories as poll_factories

register(poll_factories.PollFactory)
register(poll_factories.QuestionFactory)
register(poll_factories.ChoiceFactory)
register(poll_factories.VoteFactory)
