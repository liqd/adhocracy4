import factory
from allauth.socialaccount.models import SocialAccount

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.servicekonto.provider import ServiceKontoProvider


class SocialAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SocialAccount

    user = factory.SubFactory(a4_factories.USER_FACTORY)
    uid = "1"
    provider = ServiceKontoProvider.id
