import factory

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.extprojects import models as extproject_models


class ExternalProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = extproject_models.ExternalProject

    name = factory.Faker("sentence", nb_words=4)
    organisation = factory.SubFactory(a4_factories.ORGANISATION_FACTORY)
