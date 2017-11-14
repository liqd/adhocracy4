import factory

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.documents import models as document_models


class ChapterFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = document_models.Chapter

    name = factory.Faker('sentence')
    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    module = factory.SubFactory(a4_factories.ModuleFactory)
    weight = factory.Faker('random_number')


class ParagraphFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = document_models.Paragraph

    name = factory.Faker('sentence')
    text = 'text'
    weight = factory.Faker('random_number')
    chapter = factory.SubFactory(ChapterFactory)
