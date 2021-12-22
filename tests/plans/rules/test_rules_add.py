import pytest
import rules

from adhocracy4.test.helpers import setup_users
from tests.helpers import setup_group_users

perm_name = 'meinberlin_plans.add_plan'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_rule(plan, user_factory, group_factory,
              project, user):

    plan.projects.add(project)

    anonymous, moderator, initiator = setup_users(project)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    assert not rules.has_perm(perm_name, anonymous, plan.organisation)
    assert not rules.has_perm(perm_name, user, plan.organisation)
    assert not rules.has_perm(perm_name, moderator, plan.organisation)
    assert not rules.has_perm(perm_name, group_member_out, plan.organisation)
    assert not rules.has_perm(perm_name, group_member_in_project,
                              plan.organisation)
    assert rules.has_perm(perm_name, group_member_in_orga, plan.organisation)
    assert rules.has_perm(perm_name, initiator, plan.organisation)
