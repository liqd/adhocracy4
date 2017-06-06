import factory
from allauth.socialaccount.models import SocialAccount
from tests.factories import UserFactory

from apps.servicekonto.provider import ServiceKontoProvider


class SocialAccountFactory(factory.DjangoModelFactory):

    class Meta:
        model = SocialAccount

    user = factory.SubFactory(UserFactory)
    uid = '1'
    provider = ServiceKontoProvider.id
