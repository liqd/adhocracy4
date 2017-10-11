import factory

from adhocracy4.categories.models import Category
from adhocracy4.test.factories import ModuleFactory


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category

    name = factory.Faker('job')
    module = factory.SubFactory(ModuleFactory)
