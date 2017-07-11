import factory

from adhocracy4.test.factories import ModuleFactory
from apps.topicprio import models
from tests.factories import UserFactory


class TopicFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Topic

    creator = factory.SubFactory(UserFactory)
    module = factory.SubFactory(ModuleFactory)
