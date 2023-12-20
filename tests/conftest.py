import factory
import pytest
from celery import Celery
from django.core.cache import cache
from django.urls import reverse
from pytest_factoryboy import register
from rest_framework.test import APIClient

from adhocracy4.test import factories as a4_factories
from adhocracy4.test.factories import categories as a4_category_factories
from adhocracy4.test.factories import labels as a4_label_factories
from adhocracy4.test.factories.maps import AreaSettingsFactory
from meinberlin.test import factories
from meinberlin.test.factories.activities import ActivityFactory
from meinberlin.test.factories.bplan import BplanFactory
from meinberlin.test.factories.extprojects import ExternalProjectFactory
from meinberlin.test.factories.likes import LikeFactory
from meinberlin.test.factories.organisations import OrganisationFactory
from meinberlin.test.factories.plans import PlanFactory


def pytest_configure(config):
    Celery(task_always_eager=True)


register(factories.UserFactory)
register(factories.UserFactory, "user2")
register(factories.AdminFactory, "admin")
register(OrganisationFactory)
register(factories.CommentFactory)
register(factories.RatingFactory)
register(factories.ModeratorFeedbackFactory)
register(a4_category_factories.CategoryFactory)
register(a4_category_factories.CategoryAliasFactory)
register(factories.AdministrativeDistrictFactory)
register(factories.LiveStreamFactory)
register(a4_label_factories.LabelFactory)
register(a4_label_factories.LabelAliasFactory)
register(ActivityFactory)
register(PlanFactory)
register(ExternalProjectFactory)
register(BplanFactory)
register(LikeFactory)

register(a4_factories.GroupFactory)
register(a4_factories.ProjectFactory)
register(a4_factories.PhaseFactory)
register(a4_factories.ModuleFactory)
register(AreaSettingsFactory)


@pytest.fixture
def apiclient():
    return APIClient()


@pytest.fixture
def smallImage():
    return factory.django.ImageField(width=200, height=200)


@pytest.fixture
def bigImage():
    return factory.django.ImageField(width=1400, height=1400)


@pytest.fixture
def ImageBMP():
    return factory.django.ImageField(width=1400, height=1400, format="BMP")


@pytest.fixture
def ImagePNG():
    return factory.django.ImageField(width=1400, height=1400, format="PNG")


@pytest.fixture
def image_factory():
    return factories.ImageFactory()


@pytest.fixture
def login_url():
    return reverse("account_login")


@pytest.fixture
def logout_url():
    return reverse("account_logout")


@pytest.fixture
def signup_url():
    return reverse("account_signup")


@pytest.fixture(scope="function", autouse=True)
def cache_clear():
    yield cache
    cache.clear()
