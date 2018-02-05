from pytest_factoryboy import register

from adhocracy4.test.factories.maps import AreaSettingsFactory
from . import factories

register(factories.DashboardTestComponentFactory)
register(AreaSettingsFactory)
