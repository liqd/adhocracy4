import factory

from adhocracy4.test.factories import UserFactory

from .models import ModeratorStatement


class ModeratorStatementFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ModeratorStatement

    statement = factory.Faker('text')
    creator = factory.SubFactory(UserFactory)
