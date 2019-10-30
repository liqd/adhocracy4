import factory

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.bplan import models as bplan_models


class BplanFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = bplan_models.Bplan

    name = factory.Faker('sentence', nb_words=4)
    organisation = factory.SubFactory(a4_factories.ORGANISATION_FACTORY)
