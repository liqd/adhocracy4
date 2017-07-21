import factory
from allauth.socialaccount.models import SocialAccount

from meinberlin.apps.servicekonto.provider import ServiceKontoProvider
from tests.factories import UserFactory


class SocialAccountFactory(factory.DjangoModelFactory):

    class Meta:
        model = SocialAccount

    user = factory.SubFactory(UserFactory)
    uid = '1'
    provider = ServiceKontoProvider.id
