import factory

from meinberlin.apps.bplan import models as bplan_models

from . import OrganisationFactory


class BplanFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = bplan_models.Bplan

    name = factory.Faker('sentence')
    organisation = factory.SubFactory(OrganisationFactory)
