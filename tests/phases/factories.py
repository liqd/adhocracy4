import factory
from dateutil.parser import parse

from euth.phases import models

from ..modules import factories as module_factories


class PhaseFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Phase

    name = factory.Sequence(lambda n: '{}. phase'.format(n))
    description = factory.Faker('text')
    type = 'blog:020:phase'
    module = factory.SubFactory(module_factories.ModuleFactory)
    start_date = parse('2013-01-02 00:00:00 UTC')
    end_date = parse('2013-01-03 00:00:00 UTC')
