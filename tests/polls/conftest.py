from pytest_factoryboy import register

from adhocracy4.test.factories import polls as a4_poll_factories

register(a4_poll_factories.AnswerFactory)
register(a4_poll_factories.ChoiceFactory)
register(a4_poll_factories.OtherVoteFactory)
register(a4_poll_factories.PollFactory)
register(a4_poll_factories.QuestionFactory)
register(a4_poll_factories.VoteFactory)
