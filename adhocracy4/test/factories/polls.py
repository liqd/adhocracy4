import factory
from django.conf import settings

from adhocracy4.polls import models
from adhocracy4.test.factories import ModuleFactory
from adhocracy4.test.factories import UserFactory

USER_FACTORY = getattr(settings, "A4_USER_FACTORY", UserFactory)


class PollFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Poll

    creator = factory.SubFactory(USER_FACTORY)
    module = factory.SubFactory(ModuleFactory)


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Question

    label = factory.Faker("sentence", nb_words=4)
    weight = factory.Faker("random_number", digits=4)
    poll = factory.SubFactory(PollFactory)


class OpenQuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Question

    label = factory.Faker("sentence", nb_words=4)
    weight = factory.Faker("random_number", digits=4)
    poll = factory.SubFactory(PollFactory)
    is_open = True


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Answer

    creator = factory.SubFactory(USER_FACTORY)
    answer = factory.Faker("sentence", nb_words=10)
    question = factory.SubFactory(OpenQuestionFactory)


class ChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Choice

    label = factory.Faker("sentence", nb_words=4)
    weight = factory.Faker("random_number", digits=4)
    question = factory.SubFactory(QuestionFactory)


class OtherChoiceFactory(ChoiceFactory):

    is_other_choice = True


class VoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Vote

    creator = factory.SubFactory(USER_FACTORY)
    choice = factory.SubFactory(ChoiceFactory)


class VoteOnOtherChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Vote

    creator = factory.SubFactory(USER_FACTORY)
    choice = factory.SubFactory(OtherChoiceFactory)


class OtherVoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.OtherVote

    vote = factory.SubFactory(VoteOnOtherChoiceFactory)
    answer = factory.Faker("sentence", nb_words=4)
