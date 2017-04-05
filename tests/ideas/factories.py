import factory
from tests.factories import UserFactory

from adhocracy4.test.factories import ModuleFactory
from apps.ideas import models as idea_models


class IdeaFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = idea_models.Idea

    name = factory.Faker('name')
    description = '<script>alert("hello");</script>Description'
    creator = factory.SubFactory(UserFactory)
    module = factory.SubFactory(ModuleFactory)
