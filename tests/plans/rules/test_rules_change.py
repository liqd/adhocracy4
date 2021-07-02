import pytest
import rules

from adhocracy4.test.helpers import setup_users

perm_name = 'meinberlin_plans.change_plan'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_rule(plan, user, project):
    plan.projects.add(project)
    anonymous, moderator, initiator = setup_users(project)

    assert not rules.has_perm(perm_name, anonymous, plan)
    assert not rules.has_perm(perm_name, user, plan)
    assert not rules.has_perm(perm_name, moderator, plan)
    assert rules.has_perm(perm_name, initiator, plan)
