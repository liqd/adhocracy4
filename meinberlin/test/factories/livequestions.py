import factory

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.livequestions import models
from meinberlin.test.factories import CategoryFactory


class LiveQuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LiveQuestion

    text = factory.Faker("text", max_nb_chars=50)
    category = factory.SubFactory(CategoryFactory)
    module = factory.SubFactory(a4_factories.ModuleFactory)
