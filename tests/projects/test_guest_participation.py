from unittest.mock import patch

import pytest
import rules


@pytest.mark.django_db
def test_has_member_blocks_guest_when_disabled(project_factory, user_factory):
    project = project_factory(is_draft=False)
    project.allow_guest_users = False
    project.save()
    user = user_factory()

    assert project.has_member(user) is True

    with patch("adhocracy4.projects.models.is_guest_user", return_value=True):
        assert project.has_member(user) is False


@pytest.mark.django_db
def test_has_member_allows_guest_when_enabled(project_factory, user_factory):
    project = project_factory(is_draft=False)
    project.allow_guest_users = True
    project.save()
    user = user_factory()

    with patch("adhocracy4.projects.models.is_guest_user", return_value=True):
        assert project.has_member(user) is True


@pytest.mark.django_db
def test_participate_in_project_guest_blocked_when_disabled(
    project_factory, user_factory
):
    project = project_factory(is_draft=False)
    project.allow_guest_users = False
    project.save()
    user = user_factory()

    assert rules.has_perm("a4projects.participate_in_project", user, project) is True

    with patch("adhocracy4.projects.guest_users.is_guest_user", return_value=True):
        assert (
            rules.has_perm("a4projects.participate_in_project", user, project) is False
        )


@pytest.mark.django_db
def test_view_project_guest_can_still_view_when_disabled(project_factory, user_factory):
    project = project_factory(is_draft=False)
    project.allow_guest_users = False
    project.save()
    user = user_factory()

    with patch("adhocracy4.projects.guest_users.is_guest_user", return_value=True):
        assert rules.has_perm("a4projects.view_project", user, project) is True
