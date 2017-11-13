import factory

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.mapideas import models


class MapIdeaFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.MapIdea

    name = factory.Faker('sentence')
    description = 'Description'
    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    module = factory.SubFactory(a4_factories.ModuleFactory)
    point_label = factory.Faker('address')
    point = {
        'type': 'Feature',
        'properties': {},
        'geometry': {'type': 'Point',
                     'coordinates': [13.447437286376953, 52.51518602243137]}
    }
