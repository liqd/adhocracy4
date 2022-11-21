import pytest
import rules

from adhocracy4.test.helpers import setup_users
from meinberlin.test.helpers import setup_group_members

perm_name = 'meinberlin_plans.add_plan'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_rule(plan, user_factory, group_factory,
              project, user):

    plan.projects.add(project)

    anonymous, moderator, initiator = setup_users(project)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_group_members(project, group_factory, user_factory)

    assert not rules.has_perm(perm_name, anonymous, plan.organisation)
    assert not rules.has_perm(perm_name, user, plan.organisation)
    assert not rules.has_perm(perm_name, moderator, plan.organisation)
    assert not rules.has_perm(perm_name, group_member_out, plan.organisation)
    assert not rules.has_perm(perm_name, group_member_in_pro,
                              plan.organisation)
    assert rules.has_perm(perm_name, group_member_in_org, plan.organisation)
    assert rules.has_perm(perm_name, initiator, plan.organisation)
