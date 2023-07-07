import factory

from adhocracy4.test import factories as a4_factories
from adhocracy4.test.factories import categories as a4_category_factories
from meinberlin.apps.livequestions import models


class LiveQuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LiveQuestion

    text = factory.Faker("text", max_nb_chars=50)
    category = factory.SubFactory(a4_category_factories.CategoryFactory)
    module = factory.SubFactory(a4_factories.ModuleFactory)
