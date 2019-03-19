from pytest_factoryboy import register

from adhocracy4.test.factories.organisations import OrganisationFactory
from adhocracy4.test.factories.maps import AreaSettingsFactory
from . import factories

register(OrganisationFactory)
register(factories.DashboardTestComponentFactory)
register(AreaSettingsFactory)
