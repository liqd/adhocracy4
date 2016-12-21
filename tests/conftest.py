import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from tests.images import factories as img_factories
from tests.apps.questions import factories as q_factories
from adhocracy4.test import factories



@pytest.fixture
def apiclient():
    return APIClient()


@pytest.fixture
def image_factory():
    return  img_factories.ImageFactory()


register(factories.UserFactory)
register(factories.UserFactory, 'another_user')
register(factories.UserFactory, 'staff_user', is_staff=True)
register(factories.OrganisationFactory)
register(factories.ProjectFactory)
register(factories.ModuleFactory)
register(factories.PhaseFactory)
register(q_factories.QuestionFactory)
