import factory

from adhocracy4.test.factories import AdministrativeDistrictFactory
from adhocracy4.test.factories import ProjectFactory
from meinberlin.apps.cms.models import storefronts


class StorefrontFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = storefronts.Storefront


class StorefrontItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = storefronts.StorefrontItem

    district = factory.SubFactory(AdministrativeDistrictFactory)
    project = factory.SubFactory(ProjectFactory)
