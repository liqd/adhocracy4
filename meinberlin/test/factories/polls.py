import factory

from adhocracy4.polls import models
from adhocracy4.test import factories

from . import UserFactory


class PollFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Poll

    creator = factory.SubFactory(UserFactory)
    module = factory.SubFactory(factories.ModuleFactory)


class QuestionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Question

    label = factory.Faker('sentence', nb_words=4)
    weight = factory.Faker('random_number', digits=4)
    poll = factory.SubFactory(PollFactory)


class ChoiceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Choice

    label = factory.Faker('sentence', nb_words=4)
    question = factory.SubFactory(QuestionFactory)


class VoteFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Vote

    creator = factory.SubFactory(UserFactory)
    choice = factory.SubFactory(ChoiceFactory)
