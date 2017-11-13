from pytest_factoryboy import register

from meinberlin.apps.test.factories import plans as plan_factories

register(plan_factories.PlanFactory)
