import factory

from adhocracy4.test.factories import ProjectFactory
from apps.offlineevents import models
from tests.factories import UserFactory


class OfflineEventFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.OfflineEvent

    creator = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)
    date = factory.Faker('date')
