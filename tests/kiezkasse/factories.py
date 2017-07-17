import factory

from adhocracy4.test.factories import ModuleFactory
from apps.kiezkasse import models
from tests.factories import UserFactory


class ProposalFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Proposal

    creator = factory.SubFactory(UserFactory)
    module = factory.SubFactory(ModuleFactory)
