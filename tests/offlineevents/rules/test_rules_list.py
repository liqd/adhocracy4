import pytest
import rules

from adhocracy4.test.helpers import setup_users
from tests.helpers import setup_group_users

perm_name = 'meinberlin_offlineevents.list_offlineevent'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_rule(offline_event, user_factory, group_factory,
              user):

    project = offline_event.project

    anonymous, moderator, initiator = setup_users(project)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    assert not rules.has_perm(perm_name, anonymous, project)
    assert not rules.has_perm(perm_name, user, project)
    assert not rules.has_perm(perm_name, group_member_in_orga, project)
    assert not rules.has_perm(perm_name, group_member_out, project)
    assert not rules.has_perm(perm_name, moderator, project)
    assert rules.has_perm(perm_name, group_member_in_project, project)
    assert rules.has_perm(perm_name, initiator, project)
