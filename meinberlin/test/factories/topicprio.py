import factory

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.topicprio import models


class TopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Topic

    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    module = factory.SubFactory(a4_factories.ModuleFactory)
