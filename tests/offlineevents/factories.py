import factory
from dateutil.parser import parse

from adhocracy4.test.factories import ProjectFactory
from meinberlin.apps.offlineevents import models
from tests.factories import UserFactory


class OfflineEventFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.OfflineEvent

    creator = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)
    date = parse('2013-01-02 00:00:00 UTC')
