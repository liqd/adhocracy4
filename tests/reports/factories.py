import factory

from adhocracy4.test import factories as a4_factories
from tests.apps.questions import factories


class ReportFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'a4reports.Report'

    description = factory.Faker('text')
    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    content_object = factory.SubFactory(factories.QuestionFactory)
