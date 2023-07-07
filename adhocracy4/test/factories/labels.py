import factory

from adhocracy4.labels.models import Label
from adhocracy4.labels.models import LabelAlias
from adhocracy4.test.factories import ModuleFactory


class LabelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Label

    name = factory.Faker("name")
    module = factory.SubFactory(ModuleFactory)


class LabelAliasFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LabelAlias

    title = factory.Faker("name")
    description = factory.Faker("sentence", nb_words=4)
    module = factory.SubFactory(ModuleFactory)
