import pytest

from adhocracy4.follows.models import Follow


@pytest.mark.django_db
def test_autofollow_moderator(project, user, user2):
    project.moderators.add(user)
    assert Follow.objects.filter(project=project, creator=user).exists()

    user2.project_moderator.add(project)
    assert Follow.objects.filter(project=project, creator=user2).exists()
