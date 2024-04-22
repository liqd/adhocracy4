from pytest_factoryboy import register

from adhocracy4.test.factories import categories as category_factories
from adhocracy4.test.factories.maps import AreaSettingsFactory

register(category_factories.CategoryFactory)
register(category_factories.CategoryAliasFactory)
register(AreaSettingsFactory)
