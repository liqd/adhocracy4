import factory

from adhocracy4.test.factories import ModuleFactory
from meinberlin.apps.maptopicprio import models

from . import UserFactory


class MaptopicFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.MapTopic

    name = factory.Faker('sentence')
    description = 'Description'
    creator = factory.SubFactory(UserFactory)
    module = factory.SubFactory(ModuleFactory)
    point_label = factory.Faker('address')
    point = {
        'type': 'Feature',
        'properties': {},
        'geometry': {'type': 'Point',
                     'coordinates': [13.447437286376953, 52.51518602243137]}
    }
