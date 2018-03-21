import factory

from dateutil.parser import parse


class OfflineEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'a4offlineevents.OfflineEvent'

    slug = factory.Faker('slug')
    name = factory.Faker('sentence')
    date = parse('2013-01-02 00:00:00 UTC')
    description = factory.Faker('text', max_nb_chars=120)
    project = factory.SubFactory('adhocracy4.test.factories.ProjectFactory')


class OfflineEventDocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'a4offlineevents.OfflineEventDocument'

    title = factory.Faker('sentence')
    document = factory.django.FileField()
    offlineevent = factory.SubFactory(OfflineEventFactory)
