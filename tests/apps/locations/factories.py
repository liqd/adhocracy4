from adhocracy4.test import factories

from . import models


class LocationFactory(factories.ItemFactory):

    class Meta:
        model = models.Location

    point = {
        'type': 'Feature',
        'properties': {},
        'geometry': {
            'type': 'Point', 'coordinates': [1.0, 1.0]
        }
    }
