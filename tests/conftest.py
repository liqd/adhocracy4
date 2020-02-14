import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from adhocracy4.test import factories
from adhocracy4.test import helpers
from tests.apps.locations import factories as location_factories
from tests.apps.organisations.factories import MemberFactory
from tests.apps.organisations.factories import OrganisationFactory
from tests.apps.questions import factories as q_factories
from tests.images import factories as img_factories


def pytest_configure(config):
    # Patch email background_task decorators for all tests
    helpers.patch_background_task_decorator('adhocracy4.emails.tasks')


@pytest.fixture
def apiclient():
    return APIClient()


@pytest.fixture
def image_factory():
    return img_factories.ImageFactory()


register(OrganisationFactory)
register(factories.UserFactory)
register(MemberFactory)
register(factories.GroupFactory)
register(factories.AdminFactory, 'admin')
register(factories.UserFactory, 'another_user')
register(factories.UserFactory, 'staff_user', is_staff=True)
register(factories.ProjectFactory)
register(factories.ModuleFactory)
register(factories.PhaseFactory)
register(q_factories.QuestionFactory)
register(location_factories.LocationFactory)
