import factory

from adhocracy4.follows import models as follow_models
from adhocracy4.test import factories as a4_factories
from meinberlin.apps.newsletters import models


# FIXME: copied from core
class FollowFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = follow_models.Follow

    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    project = factory.SubFactory(a4_factories.ProjectFactory)


class NewsletterFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Newsletter

    sender = factory.Faker('email')
    sender_name = factory.Faker('name')
    subject = factory.Faker('sentence', nb_words=4)
    body = factory.Faker('text')

    receivers = models.PROJECT

    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    project = factory.SubFactory(a4_factories.ProjectFactory)
    organisation = factory.SubFactory(a4_factories.ORGANISATION_FACTORY)
