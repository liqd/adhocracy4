import factory

from adhocracy4.test import factories as a4_factories
from apps.budgeting import models as budgeting_models
from apps.moderatorfeedback import models as moderatorfeedback_models
from tests import factories


class ProposalFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = budgeting_models.Proposal

    name = factory.Faker('name')
    description = 'Description'
    creator = factory.SubFactory(factories.UserFactory)
    module = factory.SubFactory(a4_factories.ModuleFactory)

    moderator_statement = factory.SubFactory(
        factories.ModeratorStatementFactory)
    moderator_feedback = moderatorfeedback_models.DEFAULT_CHOICES[0][0]

    point_label = factory.Faker('address')
    point = {
        'type': 'Feature',
        'properties': {},
        'geometry': {'type': 'Point',
                     'coordinates': [13.447437286376953, 52.51518602243137]}
    }
