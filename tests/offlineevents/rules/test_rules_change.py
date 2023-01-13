import pytest
import rules

from adhocracy4.test.helpers import setup_users
from meinberlin.test.helpers import setup_group_members

perm_name = "meinberlin_offlineevents.change_offlineevent"


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_rule(offline_event, user_factory, group_factory, user):

    project = offline_event.project

    anonymous, moderator, initiator = setup_users(project)
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)

    assert not rules.has_perm(perm_name, anonymous, project)
    assert not rules.has_perm(perm_name, user, project)
    assert not rules.has_perm(perm_name, group_member_in_org, project)
    assert not rules.has_perm(perm_name, group_member_out, project)
    assert not rules.has_perm(perm_name, moderator, project)
    assert rules.has_perm(perm_name, group_member_in_pro, project)
    assert rules.has_perm(perm_name, initiator, project)
