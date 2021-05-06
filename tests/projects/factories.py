import factory

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.projects import models


class ParticipantInviteFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.ParticipantInvite

    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    project = factory.SubFactory(a4_factories.ProjectFactory)
    email = factory.Sequence(lambda n: 'user%d@liqd.net' % n)


class ModeratorInviteFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.ModeratorInvite

    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    project = factory.SubFactory(a4_factories.ProjectFactory)
    email = factory.Sequence(lambda n: 'user%d@liqd.net' % n)
