import pytest

from adhocracy4.follows.models import Follow


@pytest.mark.django_db
def test_autofollow_moderator(project, user, user2):
    project.moderators.add(user)
    assert Follow.objects.filter(project=project, creator=user).exists()

    user2.project_moderator.add(project)
    assert Follow.objects.filter(project=project, creator=user2).exists()


@pytest.mark.django_db
def test_autofollow_participant(project_factory, user, user2):
    project = project_factory(is_public=False)

    project.participants.add(user)
    assert Follow.objects.filter(project=project, creator=user).exists()

    user2.project_participant.add(project)
    assert Follow.objects.filter(project=project, creator=user2).exists()


@pytest.mark.django_db
def test_autounfollow_participant_remove(project_factory, admin, user):
    project = project_factory(is_public=False)
    moderator = project.moderators.first()

    project.participants.add(moderator, user, admin)
    project.participants.remove(moderator, user, admin)
    assert not Follow.objects.filter(project=project, creator=user).exists()
    assert Follow.objects.filter(project=project, creator=moderator).exists()
    assert Follow.objects.filter(project=project, creator=admin).exists()

    project.participants.add(moderator, user, admin)
    user.project_participant.remove(project)
    moderator.project_participant.remove(project)
    admin.project_participant.remove(project)
    assert not Follow.objects.filter(project=project, creator=user).exists()
    assert Follow.objects.filter(project=project, creator=moderator).exists()
    assert Follow.objects.filter(project=project, creator=admin).exists()


@pytest.mark.django_db
def test_autounfollow_participant_clear(project_factory, admin, user):
    project = project_factory(is_public=False)
    moderator = project.moderators.first()

    project.participants.add(moderator, user, admin)
    project.participants.clear()
    assert not Follow.objects.filter(project=project, creator=user).exists()
    assert Follow.objects.filter(project=project, creator=moderator).exists()
    assert Follow.objects.filter(project=project, creator=admin).exists()

    project.participants.add(moderator, user, admin)
    user.project_participant.clear()
    moderator.project_participant.clear()
    admin.project_participant.clear()
    assert not Follow.objects.filter(project=project, creator=user).exists()
    assert Follow.objects.filter(project=project, creator=moderator).exists()
    assert Follow.objects.filter(project=project, creator=admin).exists()
