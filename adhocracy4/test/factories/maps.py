from adhocracy4.maps.models import AreaSettings

from . import SettingsFactory


class AreaSettingsFactory(SettingsFactory):
    class Meta:
        model = AreaSettings

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
