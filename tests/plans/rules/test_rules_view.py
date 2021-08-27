import pytest
import rules

from adhocracy4.test.helpers import setup_users

perm_name = 'meinberlin_plans.view_plan'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_rule(plan, user, project):
    plan.projects.add(project)
    anonymous, moderator, initiator = setup_users(project)

    assert rules.has_perm(perm_name, anonymous, plan)
    assert rules.has_perm(perm_name, user, plan)
    assert rules.has_perm(perm_name, moderator, plan)
    assert rules.has_perm(perm_name, initiator, plan)


@pytest.mark.django_db
def test_rule_plan_draft(plan_factory, user, project):
    plan = plan_factory(is_draft=True, organisation=project.organisation)
    plan.projects.add(project)
    anonymous, moderator, initiator = setup_users(project)

    assert not rules.has_perm(perm_name, anonymous, plan)
    assert not rules.has_perm(perm_name, user, plan)
    assert not rules.has_perm(perm_name, moderator, plan)
    assert rules.has_perm(perm_name, initiator, plan)
