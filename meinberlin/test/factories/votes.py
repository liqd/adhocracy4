import string

import factory
from factory import fuzzy

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.votes import models as voting_models


class VotingTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = voting_models.VotingToken

    token = fuzzy.FuzzyText(length=12, chars=string.ascii_letters + string.digits)
    module = factory.SubFactory(a4_factories.ModuleFactory)
    allowed_votes = 5
    is_active = True


class TokenVoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = voting_models.TokenVote
