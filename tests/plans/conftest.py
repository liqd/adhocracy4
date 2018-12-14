from pytest_factoryboy import register

from adhocracy4.test.factories import AdministrativeDistrictFactory
from adhocracy4.test.factories import ProjectFactory
from meinberlin.test.factories import plans as plan_factories

register(ProjectFactory)
register(AdministrativeDistrictFactory)
register(plan_factories.PlanFactory)
