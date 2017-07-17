import factory

from adhocracy4.test.factories import ModuleFactory
from apps.budgeting import models
from apps.moderatorfeedback import models as moderatorfeedback_models
from tests.factories import ModeratorStatementFactory
from tests.factories import UserFactory


class ProposalFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Proposal

    name = factory.Faker('name')
    description = 'Description'
    creator = factory.SubFactory(UserFactory)
    module = factory.SubFactory(ModuleFactory)

    moderator_statement = factory.SubFactory(ModeratorStatementFactory)
    moderator_feedback = moderatorfeedback_models.DEFAULT_CHOICES[0][0]

    point_label = factory.Faker('address')
    point = {
        'type': 'Feature',
        'properties': {},
        'geometry': {'type': 'Point',
                     'coordinates': [13.447437286376953, 52.51518602243137]}
    }
