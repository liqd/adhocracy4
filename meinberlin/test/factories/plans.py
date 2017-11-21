import factory

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.plans import models as plan_models


class PlanFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = plan_models.Plan

    title = factory.Faker('sentence')
    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    organisation = factory.SubFactory(a4_factories.ORGANISATION_FACTORY)
    project = factory.SubFactory(a4_factories.ProjectFactory)
    point = {
        'type': 'Feature',
        'properties': {},
        'geometry': {'type': 'Point',
                     'coordinates': [13.447437286376953, 52.51518602243137]}
    }
    contact = ''
    category = ''
    status = plan_models.STATUS_TODO
    participation = plan_models.PARTICIPATION_UNDECIDED
