import factory

from adhocracy4.test.factories import UserFactory

from .models import ModeratorFeedback


class ModeratorFeedbackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ModeratorFeedback

    feedback_text = factory.Faker("text")
    creator = factory.SubFactory(UserFactory)
