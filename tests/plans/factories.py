import factory

from adhocracy4.test.factories import ProjectFactory
from meinberlin.apps.plans import models as plan_models
from tests.factories import OrganisationFactory
from tests.factories import UserFactory


class PlanFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = plan_models.Plan

    title = factory.Faker('sentence')
    creator = factory.SubFactory(UserFactory)
    organisation = factory.SubFactory(OrganisationFactory)
    project = factory.SubFactory(ProjectFactory)
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
