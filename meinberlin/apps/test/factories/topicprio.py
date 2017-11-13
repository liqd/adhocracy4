import factory

from adhocracy4.test.factories import ModuleFactory
from meinberlin.apps.topicprio import models

from . import UserFactory


class TopicFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Topic

    creator = factory.SubFactory(UserFactory)
    module = factory.SubFactory(ModuleFactory)
