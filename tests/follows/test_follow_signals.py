import pytest

from adhocracy4.follows import models
from adhocracy4.follows.signals import autofollow_hook


@pytest.mark.django_db
def test_autofollow_hook(user, question_factory):

    question = question_factory(creator=user)
    autofollow_hook(question)
    follow = models.Follow.objects.get(creator=user, project=question.project)
    assert follow
    assert follow.enabled

    follow.enabled = False
    follow.save()

    question = question_factory(creator=user, module=question.module)
    autofollow_hook(question)
    follow = models.Follow.objects.get(creator=user, project=question.project)
    assert follow
    assert not follow.enabled
