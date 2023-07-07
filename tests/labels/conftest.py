from pytest_factoryboy import register

from adhocracy4.test.factories import labels as label_factories
from tests.apps.ideas import factories as idea_factories

register(idea_factories.IdeaFactory)
register(label_factories.LabelFactory)
register(label_factories.LabelAliasFactory)
