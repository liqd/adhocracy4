from pytest_factoryboy import register

from tests.apps.ideas import factories as idea_factories

from .factories import LabelFactory

register(LabelFactory)
register(idea_factories.IdeaFactory)
