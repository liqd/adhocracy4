import pytest
import rules

from adhocracy4.test.helpers import setup_users
from meinberlin.test.helpers import setup_group_members

perm_name = 'meinberlin_plans.view_plan'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_rule(plan, user_factory, group_factory,
              project, user):

    plan.projects.add(project)

    anonymous, moderator, initiator = setup_users(project)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_group_members(project, group_factory, user_factory)

    assert rules.has_perm(perm_name, anonymous, plan)
    assert rules.has_perm(perm_name, user, plan)
    assert rules.has_perm(perm_name, moderator, plan)
    assert rules.has_perm(perm_name, initiator, plan)
    assert rules.has_perm(perm_name, group_member_in_org, plan)
    assert rules.has_perm(perm_name, group_member_out, plan)
    assert rules.has_perm(perm_name, group_member_in_pro, plan)


@pytest.mark.django_db
def test_rule_plan_draft(plan_factory, user_factory, group_factory,
                         project, user):

    plan = plan_factory(is_draft=True, organisation=project.organisation)
    plan.projects.add(project)

    anonymous, moderator, initiator = setup_users(project)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_group_members(project, group_factory, user_factory)

    assert not rules.has_perm(perm_name, anonymous, plan)
    assert not rules.has_perm(perm_name, user, plan)
    assert not rules.has_perm(perm_name, moderator, plan)
    assert not rules.has_perm(perm_name, group_member_in_org, plan)
    assert not rules.has_perm(perm_name, group_member_out, plan)
    assert not rules.has_perm(perm_name, group_member_in_pro, plan)
    assert rules.has_perm(perm_name, initiator, plan)
