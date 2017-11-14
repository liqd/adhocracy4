from pytest_factoryboy import register

from meinberlin.test.factories import extprojects as extproject_factories

register(extproject_factories.ExternalProjectFactory)
