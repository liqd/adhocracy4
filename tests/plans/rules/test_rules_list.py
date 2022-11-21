import pytest
import rules

from adhocracy4.test.helpers import setup_users
from meinberlin.test.helpers import setup_group_members

perm_name = 'meinberlin_plans.list_plan'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_rule(plan, user_factory, group_factory,
              project, user):

    plan.projects.add(project)

    anonymous, moderator, initiator = setup_users(project)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_group_members(project, group_factory, user_factory)

    assert rules.has_perm(perm_name, anonymous, None)
    assert rules.has_perm(perm_name, user, None)
    assert rules.has_perm(perm_name, moderator, None)
    assert rules.has_perm(perm_name, initiator, None)
    assert rules.has_perm(perm_name, group_member_in_org, None)
    assert rules.has_perm(perm_name, group_member_out, None)
    assert rules.has_perm(perm_name, group_member_in_pro, None)
