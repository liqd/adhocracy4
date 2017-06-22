from pytest_factoryboy import register

from tests.ideas import factories as ideas_fatories

register(ideas_fatories.IdeaFactory)
