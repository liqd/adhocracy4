import random
import factory

from dateutil.parser import parse
from django.conf import settings
from django.contrib.auth.models import User, Group

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.projects.models import Project
from tests.apps.organisations.models import Organisation
from adhocracy4.modules.models import Module
from adhocracy4.phases.models import Phase



class OrganisationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organisation
    name = factory.Faker('company')

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)
