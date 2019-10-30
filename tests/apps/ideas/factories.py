import factory

from adhocracy4.test import factories

from . import models


class IdeaFactory(factories.ItemFactory):
    class Meta:
        model = models.Idea

    point_label = factory.Faker('address')
    point = {
        'type': 'Feature',
        'properties': {},
        'geometry': {'type': 'Point',
                     'coordinates': [13.447437286376953, 52.51518602243137]}
    }
