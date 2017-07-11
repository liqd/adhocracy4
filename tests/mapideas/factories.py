import factory

from adhocracy4.test.factories import ModuleFactory
from apps.mapideas import models
from tests.factories import UserFactory


class MapIdeaFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.MapIdea

    creator = factory.SubFactory(UserFactory)
    module = factory.SubFactory(ModuleFactory)
