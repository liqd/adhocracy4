import factory

from apps.bplan import models as bplan_models
from tests.factories import OrganisationFactory


class BplanFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = bplan_models.Bplan

    organisation = factory.SubFactory(OrganisationFactory)
