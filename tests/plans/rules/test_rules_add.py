import pytest
import rules

from adhocracy4.test.helpers import setup_users

perm_name = 'meinberlin_plans.add_plan'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_rule(plan, project, user):
    plan.projects.add(project)
    anonymous, moderator, initiator = setup_users(project)

    assert not rules.has_perm(perm_name, anonymous, plan.organisation)
    assert not rules.has_perm(perm_name, user, plan.organisation)
    assert not rules.has_perm(perm_name, moderator, plan.organisation)
    assert rules.has_perm(perm_name, initiator, plan.organisation)
