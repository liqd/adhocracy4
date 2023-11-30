import factory

from adhocracy4.test import factories as a4_factories
from adhocracy4.test.factories import AdministrativeDistrictFactory
from meinberlin.apps.plans.models import Plan


class PlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Plan

    title = factory.Faker("sentence", nb_words=4)
    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    organisation = factory.SubFactory(a4_factories.ORGANISATION_FACTORY)
    group = factory.SubFactory(a4_factories.GroupFactory)
    district = factory.SubFactory(AdministrativeDistrictFactory)
    point = {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Point",
            "coordinates": [13.447437286376953, 52.51518602243137],
        },
    }
    contact_address_text = ""
    status = Plan.STATUS_ONGOING
    participation = Plan.PARTICIPATION_INFORMATION
    is_draft = False

    @factory.post_generation
    def projects(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for project in extracted:
                self.projects.add(project)

    @factory.post_generation
    def topics(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for topic in extracted:
                self.topics.add(topic)
