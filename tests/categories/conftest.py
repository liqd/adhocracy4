from pytest_factoryboy import register

from tests.categories import factories as category_factories

register(category_factories.CategoryFactory)
