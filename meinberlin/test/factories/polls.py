import factory

from adhocracy4.polls import models
from adhocracy4.test import factories

from . import UserFactory


class PollFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Poll

    creator = factory.SubFactory(UserFactory)
    module = factory.SubFactory(factories.ModuleFactory)
