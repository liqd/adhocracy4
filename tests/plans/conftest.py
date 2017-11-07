from pytest_factoryboy import register

from tests.plans import factories as plan_factories

register(plan_factories.PlanFactory)
