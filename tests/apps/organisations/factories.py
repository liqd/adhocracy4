import factory
from django.conf import settings

from adhocracy4.test.factories import UserFactory
from tests.apps.organisations.models import Member
from tests.apps.organisations.models import Organisation


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


USER_FACTORY = getattr(settings, 'A4_USER_FACTORY', UserFactory)
ORGANISATION_FACTORY = getattr(settings, 'A4_ORGANISATION_FACTORY')


class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Member

    member = factory.SubFactory(USER_FACTORY)
    organisation = factory.SubFactory(ORGANISATION_FACTORY)
