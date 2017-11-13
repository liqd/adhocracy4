from pytest_factoryboy import register

from meinberlin.apps.test.factories import extprojects as extproject_factories

register(extproject_factories.ExternalProjectFactory)
