import factory

from adhocracy4.test import factories
from apps.documents import models as document_models
from tests.factories import UserFactory


class DocumentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = document_models.Document

    name = factory.Faker('name')
    creator = factory.SubFactory(UserFactory)
    module = factory.SubFactory(factories.ModuleFactory)


class ParagraphFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = document_models.Paragraph

    name = factory.Faker('name')
    text = 'text'
    weight = factory.Faker('random_number')
    document = factory.SubFactory(DocumentFactory)
