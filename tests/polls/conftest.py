from pytest_factoryboy import register

from . import factories

register(factories.PollFactory)
register(factories.QuestionFactory)
register(factories.ChoiceFactory)
register(factories.VoteFactory)
