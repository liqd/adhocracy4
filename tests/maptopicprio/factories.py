import factory

from adhocracy4.test.factories import ModuleFactory
from meinberlin.apps.maptopicprio import models
from tests.factories import UserFactory


class MaptopicFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.MapTopic

    creator = factory.SubFactory(UserFactory)
    module = factory.SubFactory(ModuleFactory)
