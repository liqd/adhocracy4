from pytest_factoryboy import register

from adhocracy4.test import factories


register(factories.UserFactory)
register(factories.OrganisationFactory)
register(factories.ProjectFactory)
register(factories.ModuleFactory)
register(factories.PhaseFactory)
