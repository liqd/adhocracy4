import factory

from adhocracy4.test.factories import ModuleFactory
from meinberlin.apps.ideas import models as idea_models
from tests.factories import UserFactory


class IdeaFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = idea_models.Idea

    name = factory.Faker('sentence')
    description = '<script>alert("hello");</script>Description'
    creator = factory.SubFactory(UserFactory)
    module = factory.SubFactory(ModuleFactory)
