import factory

from . import UserFactory


class OrganisationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "meinberlin_organisations.Organisation"
        django_get_or_create = ("name",)

    name = factory.Faker("company")

    @factory.post_generation
    def initiators(self, create, extracted, **kwargs):
        if not extracted:
            user = UserFactory()
            self.initiators.add(user)
            return

        if extracted:
            for user in extracted:
                self.initiators.add(user)

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)
