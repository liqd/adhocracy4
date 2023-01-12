import factory

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.budgeting import models
from meinberlin.apps.moderatorfeedback import \
    models as moderatorfeedback_models

from . import ModeratorFeedbackFactory


class ProposalFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Proposal

    name = factory.Faker('sentence', nb_words=4)
    description = 'Description'
    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    module = factory.SubFactory(a4_factories.ModuleFactory)

    moderator_feedback_text = factory.SubFactory(ModeratorFeedbackFactory)
    moderator_status = moderatorfeedback_models.DEFAULT_CHOICES[0][0]

    point_label = factory.Faker('address')
    point = {
        'type': 'Feature',
        'properties': {},
        'geometry': {'type': 'Point',
                     'coordinates': [13.447437286376953, 52.51518602243137]}
    }
