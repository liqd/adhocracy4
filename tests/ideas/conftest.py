from pytest_factoryboy import register

from meinberlin.apps.test.factories import ideas as ideas_factories

register(ideas_factories.IdeaFactory)
