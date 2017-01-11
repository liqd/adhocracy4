import factory
from django.db.models import signals

from tests.apps.fakeprojects import factories
from tests.factories import UserFactory


@factory.django.mute_signals(signals.post_save)
class CommentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'euth_comments.Comment'

    comment = factory.Faker('text')
    content_object = factory.SubFactory(factories.FakeProjectContentFactory)
    creator = factory.SubFactory(UserFactory)
