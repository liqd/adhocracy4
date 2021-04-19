import pytest
import rules

from meinberlin.test.helpers import setup_users

perm_name = 'meinberlin_organisations.change_organisation'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_rule(project, user_factory, group_factory, admin):
    organisation = project.organisation
    anonymous, moderator, initiator = setup_users(project)

    group = group_factory()
    user = user_factory()
    group_user = user_factory(groups=(group,))
    organisation.groups.add(group)

    assert not rules.has_perm(perm_name, anonymous, organisation)
    assert not rules.has_perm(perm_name, user, organisation)
    assert not rules.has_perm(perm_name, moderator, organisation)
    assert not rules.has_perm(perm_name, group_user, organisation)
    assert not rules.has_perm(perm_name, initiator, organisation)
    assert rules.has_perm(perm_name, admin, organisation)
