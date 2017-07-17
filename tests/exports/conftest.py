from pytest_factoryboy import register

from tests.budgeting import factories as budgeting_factories
from tests.ideas import factories as ideas_factories

register(ideas_factories.IdeaFactory)
register(budgeting_factories.ProposalFactory)
