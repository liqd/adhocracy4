import factory
from django.db.models import signals

from tests.apps.questions import factories
from adhocracy4.test.factories import UserFactory


@factory.django.mute_signals(signals.post_save)
class CommentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'a4comments.Comment'

    comment = factory.Faker('text')
    content_object = factory.SubFactory(factories.QuestionFactory)
    creator = factory.SubFactory(UserFactory)
