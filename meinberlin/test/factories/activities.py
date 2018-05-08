import factory
from meinberlin.apps.activities.models import Activity
from adhocracy4.test import factories as a4_factories

class ActivityFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = Activity

    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    module = factory.SubFactory(a4_factories.ModuleFactory)
