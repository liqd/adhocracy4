import factory

from adhocracy4.test import factories
from tests.apps.moderatorfeedback.factories import ModeratorStatementFactory

from . import models


class IdeaFactory(factories.ItemFactory):
    class Meta:
        model = models.Idea

    moderator_statement = factory.SubFactory(ModeratorStatementFactory)
    moderator_feedback = ("CONSIDERATION", "Under consideration")

    point_label = factory.Faker("address")
    point = {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Point",
            "coordinates": [13.447437286376953, 52.51518602243137],
        },
    }

    @factory.post_generation
    def labels(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of labels were passed in, use them
            for label in extracted:
                self.labels.add(label)
