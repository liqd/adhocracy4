import factory

from tests.factories import OrganisationFactory

from apps.bplan import models as bplan_models


class BplanFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = bplan_models.Bplan

    organisation = factory.SubFactory(OrganisationFactory)
