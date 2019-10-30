import factory
from django.db.models import signals

from adhocracy4.test.factories import UserFactory
from tests.apps.questions import factories


@factory.django.mute_signals(signals.post_save)
class CommentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'a4comments.Comment'

    comment = factory.Faker('text')
    content_object = factory.SubFactory(factories.QuestionFactory)
    creator = factory.SubFactory(UserFactory)
