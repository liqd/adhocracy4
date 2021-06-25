import factory

from adhocracy4.polls import models
from adhocracy4.test import factories
from adhocracy4.test.factories import UserFactory


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


class OpenQuestionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Question

    label = factory.Faker('sentence', nb_words=4)
    weight = factory.Faker('random_number', digits=4)
    poll = factory.SubFactory(PollFactory)
    is_open = True


class AnswerFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Answer

    creator = factory.SubFactory(UserFactory)
    answer = factory.Faker('sentence', nb_words=10)
    question = factory.SubFactory(OpenQuestionFactory)


class ChoiceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Choice

    label = factory.Faker('sentence', nb_words=4)
    question = factory.SubFactory(QuestionFactory)


class OtherChoiceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Choice

    label = factory.Faker('sentence', nb_words=4)
    question = factory.SubFactory(QuestionFactory)
    is_other_choice = True


class VoteFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Vote

    creator = factory.SubFactory(UserFactory)
    choice = factory.SubFactory(ChoiceFactory)


class VoteOnOtherChoiceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Vote

    creator = factory.SubFactory(UserFactory)
    choice = factory.SubFactory(OtherChoiceFactory)


class OtherVoteFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.OtherVote

    vote = factory.SubFactory(VoteOnOtherChoiceFactory)
    answer = factory.Faker('sentence', nb_words=4)
