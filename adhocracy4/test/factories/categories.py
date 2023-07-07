import factory

from adhocracy4.categories.models import Category
from adhocracy4.categories.models import CategoryAlias
from adhocracy4.test.factories import ModuleFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("job")
    module = factory.SubFactory(ModuleFactory)


class CategoryAliasFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CategoryAlias

    title = factory.Faker("name")
    description = factory.Faker("sentence", nb_words=4)
    module = factory.SubFactory(ModuleFactory)
