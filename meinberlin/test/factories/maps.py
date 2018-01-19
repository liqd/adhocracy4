import factory

from meinberlin.apps.maps import models as map_models


class MapPresetCategoryFactory(factory.DjangoModelFactory):

    class Meta:
        model = map_models.MapPresetCategory


class MapPresetFactory(factory.DjangoModelFactory):

    class Meta:
        model = map_models.MapPreset

    name = factory.Faker('sentence')
    polygon = {
        'type': 'Feature',
        'properties': {},
        'geometry': {'type': 'Point',
                     'coordinates': [13.447437286376953, 52.51518602243137]}
    }
    category = factory.SubFactory(MapPresetCategoryFactory)
