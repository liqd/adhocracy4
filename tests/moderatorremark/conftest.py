from pytest_factoryboy import register

from meinberlin.test.factories import ideas as ideas_factories
from meinberlin.test.factories import moderatorremarks as moderatorremarks_factories

register(ideas_factories.IdeaFactory)
register(moderatorremarks_factories.ModeratorRemarkFactory)
