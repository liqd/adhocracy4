from pytest_factoryboy import register

from meinberlin.test.factories import ideas as ideas_factories

register(ideas_factories.IdeaFactory)
