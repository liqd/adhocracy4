from factory.django import DjangoModelFactory

from adhocracy4.test import factories

from . import models


class QuestionFactory(factories.ItemFactory):
    class Meta:
        model = models.Question


class TokenVoteFactory(DjangoModelFactory):
    class Meta:
        model = models.TokenVote
