from pytest_factoryboy import register

from tests.ideas import factories as ideas_factories

register(ideas_factories.IdeaFactory)
