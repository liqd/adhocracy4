import pytest

from adhocracy4.test.helpers import setup_users
from meinberlin.apps.users.decorators import _user_is_project_admin


@pytest.mark.django_db
def test_user_is_project_admin(project, user_factory, group_factory, admin):
    anonymous, moderator, initiator = setup_users(project)
    user = user_factory()
    group = group_factory()
    group_member = user_factory.create(groups=(group,))
    project.group = group
    project.save()

    assert not _user_is_project_admin(anonymous)
    assert not _user_is_project_admin(user)
    assert not _user_is_project_admin(moderator)
    assert _user_is_project_admin(group_member)
    assert _user_is_project_admin(initiator)
    assert _user_is_project_admin(admin)
