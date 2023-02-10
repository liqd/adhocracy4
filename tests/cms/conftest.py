from pytest_factoryboy import register

from adhocracy4.test.factories import ProjectFactory
from meinberlin.test.factories import cms as cms_factories
from meinberlin.test.factories import extprojects as extproject_factories
from meinberlin.test.factories import ideas as ideas_factories
from meinberlin.test.factories import plans as plan_factories

register(ProjectFactory)
register(cms_factories.StorefrontFactory)
register(cms_factories.StorefrontItemFactory)
register(extproject_factories.ExternalProjectFactory)
register(ideas_factories.IdeaFactory)
register(plan_factories.PlanFactory)
