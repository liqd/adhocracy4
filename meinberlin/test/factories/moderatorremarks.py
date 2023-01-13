import factory

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.moderatorremark.models import ModeratorRemark
from meinberlin.test.factories.ideas import IdeaFactory


class ModeratorRemarkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ModeratorRemark

    remark = factory.Faker("text")
    item = factory.SubFactory(IdeaFactory)
    creator = factory.SubFactory(a4_factories.USER_FACTORY)
