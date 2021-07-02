import pytest

from adhocracy4.test.helpers import setup_users
from meinberlin.apps.users.decorators import _user_is_project_admin


@pytest.mark.django_db
def test_user_is_project_admin(project, user):
    anonymous, moderator, initiator = setup_users(project)
    assert not _user_is_project_admin(anonymous)
    assert not _user_is_project_admin(user)
    assert _user_is_project_admin(moderator)
    assert _user_is_project_admin(initiator)
