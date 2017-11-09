from pytest_factoryboy import register

from tests.extprojects import factories as extproject_factories

register(extproject_factories.ExternalProjectFactory)
