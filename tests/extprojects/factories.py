import factory

from meinberlin.apps.extprojects import models as extproject_models
from tests.factories import OrganisationFactory


class ExternalProjectFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = extproject_models.ExternalProject

    name = factory.Faker('sentence')
    organisation = factory.SubFactory(OrganisationFactory)
