from pytest_factoryboy import register

from tests.ideas import factories as idea_fatories

register(idea_fatories.IdeaFactory)
