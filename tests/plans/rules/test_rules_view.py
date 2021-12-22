import pytest
import rules

from adhocracy4.test.helpers import setup_users
from tests.helpers import setup_group_users

perm_name = 'meinberlin_plans.view_plan'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_rule(plan, user_factory, group_factory,
              project, user):

    plan.projects.add(project)

    anonymous, moderator, initiator = setup_users(project)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    assert rules.has_perm(perm_name, anonymous, plan)
    assert rules.has_perm(perm_name, user, plan)
    assert rules.has_perm(perm_name, moderator, plan)
    assert rules.has_perm(perm_name, initiator, plan)
    assert rules.has_perm(perm_name, group_member_in_orga, plan)
    assert rules.has_perm(perm_name, group_member_out, plan)
    assert rules.has_perm(perm_name, group_member_in_project, plan)


@pytest.mark.django_db
def test_rule_plan_draft(plan_factory, user_factory, group_factory,
                         project, user):

    plan = plan_factory(is_draft=True, organisation=project.organisation)
    plan.projects.add(project)

    anonymous, moderator, initiator = setup_users(project)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    assert not rules.has_perm(perm_name, anonymous, plan)
    assert not rules.has_perm(perm_name, user, plan)
    assert not rules.has_perm(perm_name, moderator, plan)
    assert not rules.has_perm(perm_name, group_member_in_orga, plan)
    assert not rules.has_perm(perm_name, group_member_out, plan)
    assert not rules.has_perm(perm_name, group_member_in_project, plan)
    assert rules.has_perm(perm_name, initiator, plan)
