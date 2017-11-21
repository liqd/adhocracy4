from pytest_factoryboy import register

from meinberlin.test.factories import budgeting as budgeting_factories
from meinberlin.test.factories import ideas as ideas_factories

register(ideas_factories.IdeaFactory)
register(budgeting_factories.ProposalFactory)
