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

    assert rules.has_perm(perm_name, anonymous, None)
    assert rules.has_perm(perm_name, user, None)
    assert rules.has_perm(perm_name, moderator, None)
    assert rules.has_perm(perm_name, initiator, None)
