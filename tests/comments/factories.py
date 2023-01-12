import factory
from django.db.models import signals

from adhocracy4.test.factories import UserFactory
from tests.apps.questions import factories


@factory.django.mute_signals(signals.post_save)
class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "a4comments.Comment"

    comment = factory.Faker("text")
    content_object = factory.SubFactory(factories.QuestionFactory)
    creator = factory.SubFactory(UserFactory)


@factory.django.mute_signals(signals.post_save)
class ChildCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "a4comments.Comment"

    comment = factory.Faker("text")
    content_object = factory.SubFactory(CommentFactory)
    creator = factory.SubFactory(UserFactory)
