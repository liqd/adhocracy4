import factory

from adhocracy4.follows import models as follow_models
from adhocracy4.test import factories as a4_factories
from meinberlin.apps.newsletters import models
from tests import factories


# FIXME: copied from core
class FollowFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = follow_models.Follow

    creator = factory.SubFactory(factories.UserFactory)
    project = factory.SubFactory(a4_factories.ProjectFactory)


class NewsletterFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Newsletter

    sender = factory.Faker('email')
    sender_name = factory.Faker('name')
    subject = factory.Faker('sentence')
    body = factory.Faker('text')

    receivers = models.PROJECT

    creator = factory.SubFactory(factories.UserFactory)
    project = factory.SubFactory(a4_factories.ProjectFactory)
    organisation = factory.SubFactory(factories.OrganisationFactory)
