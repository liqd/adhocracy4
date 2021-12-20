import pytest
import rules
from django.contrib.auth.models import AnonymousUser

from adhocracy4.test.helpers import setup_users

perm_name_add = 'a4projects.add_project'
perm_name_change = 'a4projects.change_project'
perm_name_delete = 'a4projects.delete_project'


def test_perm_exists():
    assert rules.perm_exists(perm_name_add)
    assert rules.perm_exists(perm_name_change)
    assert rules.perm_exists(perm_name_delete)


@pytest.mark.django_db
def test_add_project(user_factory, group_factory, organisation):
    anonymous = AnonymousUser()
    user = user_factory()
    initiator = user_factory()
    moderator = user_factory()
    admin = user_factory(is_superuser=True)

    group1 = group_factory()
    group2 = group_factory()
    group3 = group_factory()
    group_member_in = user_factory.create(groups=(group1, group2))
    group_member_out = user_factory.create(groups=(group2, group3))

    organisation.initiators.add(initiator)
    organisation.groups.add(group1)

    assert not rules.has_perm(perm_name_add, anonymous, organisation)
    assert not rules.has_perm(perm_name_add, user, organisation)
    assert not rules.has_perm(perm_name_add, moderator, organisation)
    assert not rules.has_perm(perm_name_add, group_member_out, organisation)
    assert rules.has_perm(perm_name_add, initiator, organisation)
    assert rules.has_perm(perm_name_add, admin, organisation)
    assert rules.has_perm(perm_name_add, group_member_in, organisation)


@pytest.mark.django_db
def test_change_project(user_factory, group_factory, organisation,
                        project_factory):
    user = user_factory()
    initiator = user_factory()
    admin = user_factory(is_superuser=True)

    group1 = group_factory()
    group2 = group_factory()
    group3 = group_factory()
    group4 = group_factory()
    group_member_in_orga = user_factory.create(groups=(group1, group2))
    group_member_out = user_factory.create(groups=(group2, group3))
    group_member_in_project = user_factory.create(groups=(group2, group4))

    organisation.initiators.add(initiator)
    organisation.groups.add(group1)
    project = project_factory(group=group4, organisation=organisation)
    anonymous, moderator, initiator = setup_users(project)

    assert not rules.has_perm(perm_name_change, anonymous, project)
    assert not rules.has_perm(perm_name_change, user, project)
    assert not rules.has_perm(perm_name_change, moderator, project)
    assert not rules.has_perm(perm_name_change, group_member_in_orga, project)
    assert not rules.has_perm(perm_name_change, group_member_out, project)
    assert rules.has_perm(perm_name_change, group_member_in_project, project)
    assert rules.has_perm(perm_name_change, initiator, project)
    assert rules.has_perm(perm_name_change, admin, project)


@pytest.mark.django_db
def test_delete_project(user_factory, group_factory, organisation,
                        project_factory):
    user = user_factory()
    initiator = user_factory()
    admin = user_factory(is_superuser=True)

    group1 = group_factory()
    group2 = group_factory()
    group3 = group_factory()
    group4 = group_factory()
    group_member_in_orga = user_factory.create(groups=(group1, group2))
    group_member_out = user_factory.create(groups=(group2, group3))
    group_member_in_project = user_factory.create(groups=(group2, group4))

    organisation.initiators.add(initiator)
    organisation.groups.add(group1)
    project = project_factory(group=group4, organisation=organisation)
    anonymous, moderator, initiator = setup_users(project)

    assert not rules.has_perm(perm_name_delete, anonymous, project)
    assert not rules.has_perm(perm_name_delete, user, project)
    assert not rules.has_perm(perm_name_delete, moderator, project)
    assert not rules.has_perm(perm_name_delete, group_member_in_orga, project)
    assert not rules.has_perm(perm_name_delete, group_member_out, project)
    assert not rules.has_perm(perm_name_delete, group_member_in_project,
                              project)
    assert rules.has_perm(perm_name_delete, initiator, project)
    assert rules.has_perm(perm_name_delete, admin, project)
