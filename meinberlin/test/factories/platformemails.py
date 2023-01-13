import factory

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.platformemails import models as platformemail_models


class PlatformEmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = platformemail_models.PlatformEmail

    sender = factory.Faker("email")
    sender_name = factory.Faker("name")
    subject = factory.Faker("sentence", nb_words=4)
    body = factory.Faker("text")
    creator = factory.SubFactory(a4_factories.USER_FACTORY)
