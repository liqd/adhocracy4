import factory

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.ideas import models as idea_models


class IdeaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = idea_models.Idea

    name = factory.Faker("sentence", nb_words=4)
    description = '<script>alert("hello");</script>Description'
    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    module = factory.SubFactory(a4_factories.ModuleFactory)
