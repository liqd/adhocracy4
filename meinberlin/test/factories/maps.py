import factory

from meinberlin.apps.maps import models as map_models


class MapPresetCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = map_models.MapPresetCategory


class MapPresetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = map_models.MapPreset

    name = factory.Faker("sentence", nb_words=4)
    polygon = {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Point",
            "coordinates": [13.447437286376953, 52.51518602243137],
        },
    }
    category = factory.SubFactory(MapPresetCategoryFactory)
