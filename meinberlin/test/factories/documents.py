import factory

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.documents import models as document_models


class ChapterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = document_models.Chapter

    name = factory.Faker("sentence", nb_words=4)
    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    module = factory.SubFactory(a4_factories.ModuleFactory)
    weight = factory.Faker("random_number", digits=4)


class ParagraphFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = document_models.Paragraph

    name = factory.Faker("sentence", nb_words=4)
    text = "text"
    weight = factory.Faker("random_number", digits=4)
    chapter = factory.SubFactory(ChapterFactory)
