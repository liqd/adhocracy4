import factory

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.maptopicprio import models


class MaptopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MapTopic

    name = factory.Faker("sentence", nb_words=4)
    description = "Description"
    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    module = factory.SubFactory(a4_factories.ModuleFactory)
    point_label = factory.Faker("address")
    point = {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Point",
            "coordinates": [13.447437286376953, 52.51518602243137],
        },
    }
