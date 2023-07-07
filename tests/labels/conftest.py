from pytest_factoryboy import register

from tests.apps.ideas import factories as idea_factories
from tests.labels import factories as label_factories

register(idea_factories.IdeaFactory)
register(label_factories.LabelFactory)
register(label_factories.LabelAliasFactory)
