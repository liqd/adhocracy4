from pytest_factoryboy import register

from adhocracy4.test.factories import categories as category_factories

register(category_factories.CategoryFactory)
register(category_factories.CategoryAliasFactory)
