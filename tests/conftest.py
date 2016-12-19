from pytest_factoryboy import register

from adhocracy4.test import factories


register(factories.UserFactory)
register(factories.UserFactory, 'staff_user', is_staff=True)
register(factories.OrganisationFactory)
register(factories.ProjectFactory)
register(factories.ModuleFactory)
register(factories.PhaseFactory)
