from pytest_factoryboy import register

from adhocracy4.test.factories.maps import AreaSettingsFactory
from tests.apps.organisations.factories import OrganisationFactory

from . import factories

register(OrganisationFactory)
register(factories.DashboardTestComponentFactory)
register(AreaSettingsFactory)
