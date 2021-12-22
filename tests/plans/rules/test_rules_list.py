import pytest
import rules

from adhocracy4.test.helpers import setup_users
from tests.helpers import setup_group_users

perm_name = 'meinberlin_plans.list_plan'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_rule(plan, user_factory, group_factory,
              project, user):

    plan.projects.add(project)

    anonymous, moderator, initiator = setup_users(project)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    assert rules.has_perm(perm_name, anonymous, None)
    assert rules.has_perm(perm_name, user, None)
    assert rules.has_perm(perm_name, moderator, None)
    assert rules.has_perm(perm_name, initiator, None)
    assert rules.has_perm(perm_name, group_member_in_orga, None)
    assert rules.has_perm(perm_name, group_member_out, None)
    assert rules.has_perm(perm_name, group_member_in_project, None)
