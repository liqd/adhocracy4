import factory
from dateutil.parser import parse

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.offlineevents import models


class OfflineEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.OfflineEvent

    name = factory.Faker("sentence", nb_words=4)
    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    project = factory.SubFactory(a4_factories.ProjectFactory)
    date = parse("2013-01-02 00:00:00 UTC")
