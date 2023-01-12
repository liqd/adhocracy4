import factory

from adhocracy4.follows.models import Follow

from . import ProjectFactory
from . import UserFactory


class FollowFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Follow

    creator = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)
