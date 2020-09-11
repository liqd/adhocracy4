import factory

from meinberlin.apps.likes import models
from meinberlin.test.factories.livequestions import LiveQuestionFactory


class LikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Like

    question = factory.SubFactory(LiveQuestionFactory)
