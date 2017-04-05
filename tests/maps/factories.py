
from adhocracy4.test import factories

from adhocracy4.maps import models


class AreaSettingsFactory(factories.SettingsFactory):
    class Meta:
        model = models.AreaSettings

    polygon = {
        'type': 'FeatureCollection',
        'features': [{
            'type': 'Feature',
            'properties': {},
            'geometry': {
                'type': 'Polygon',
                'coordinates': [[[0.0, 0.0], [0.0, 1.0], [1.0, 1.0]]]
            }
        }]
    }
