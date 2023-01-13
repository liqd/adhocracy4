import factory

from adhocracy4.test.factories import ModuleFactory
from meinberlin.apps.moderationtasks.models import ModerationTask


class ModerationTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ModerationTask

    name = factory.Faker("name")
    module = factory.SubFactory(ModuleFactory)
