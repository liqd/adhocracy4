import factory
from django.conf import settings

from adhocracy4.actions import models
from adhocracy4.actions import verbs
from adhocracy4.test.factories import UserFactory
from tests.apps.questions.factories import QuestionFactory

USER_FACTORY = getattr(settings, 'A4_USER_FACTORY', UserFactory)


class ActionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Action
    verb = verbs.Verbs.ADD.value
    actor = factory.SubFactory(USER_FACTORY)
    obj = factory.SubFactory(QuestionFactory)

    @factory.post_generation
    def project(obj, create, extracted, **kwargs):
        if obj.obj:
            obj.project = obj.obj.project
