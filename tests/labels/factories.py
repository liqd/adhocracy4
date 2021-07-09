import factory

from adhocracy4.labels.models import Label
from adhocracy4.test.factories import ModuleFactory


class LabelFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Label

    name = factory.Faker('name')
    module = factory.SubFactory(ModuleFactory)
