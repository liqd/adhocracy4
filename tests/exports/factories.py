import factory

from adhocracy4.test import factories as a4_factories
from apps.budgeting import models as budgeting_models
from apps.moderatorfeedback import models as moderatorfeedback_models
from tests import factories
from tests.ideas import factories as idea_factories


class RatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'a4ratings.Rating'

    value = 1
    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    content_object = factory.SubFactory(idea_factories.IdeaFactory)


class ModeratorStatementFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = moderatorfeedback_models.ModeratorStatement

    statement = factory.Faker('text')
    creator = factory.SubFactory(factories.UserFactory)


class ProposalFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = budgeting_models.Proposal

    name = factory.Faker('name')
    description = 'Description'
    creator = factory.SubFactory(factories.UserFactory)
    module = factory.SubFactory(a4_factories.ModuleFactory)

    moderator_statement = factory.SubFactory(ModeratorStatementFactory)
    moderator_feedback = moderatorfeedback_models.DEFAULT_CHOICES[0][0]

    point_label = factory.Faker('address')
    point = {
        'type': 'Feature',
        'properties': {},
        'geometry': {'type': 'Point',
                     'coordinates': [13.447437286376953, 52.51518602243137]}
    }
