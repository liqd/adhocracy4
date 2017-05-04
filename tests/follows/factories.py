import factory

from adhocracy4.follows import models as follow_models
from adhocracy4.test import factories as a4_factories


class FollowFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = follow_models.Follow

    creator = factory.SubFactory(a4_factories.UserFactory)
    project = factory.SubFactory(a4_factories.ProjectFactory)
