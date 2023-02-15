import string

import factory
from factory import fuzzy
from factory import post_generation

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.votes import models as voting_models


class TokenPackageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = voting_models.TokenPackage

    module = factory.SubFactory(a4_factories.ModuleFactory)
    downloaded = False
    size = 1


class VotingTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = voting_models.VotingToken

    token = fuzzy.FuzzyText(length=16, chars=string.ascii_letters + string.digits)
    module = factory.SubFactory(a4_factories.ModuleFactory)
    package = factory.SubFactory(TokenPackageFactory)
    allowed_votes = 5
    is_active = True

    @post_generation
    def create_hash(obj, create, extracted, **kwargs):
        token_hash = voting_models.VotingToken.hash_token(obj.token, obj.module)
        obj.token_hash = token_hash
        obj.save()


class TokenVoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = voting_models.TokenVote
