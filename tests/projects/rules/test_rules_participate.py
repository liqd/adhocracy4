import pytest
import rules
from django.contrib.auth.models import AnonymousUser

from adhocracy4.projects.enums import Access

perm_name_participate = "a4projects.participate_in_project"


def test_perm_exists():
    assert rules.perm_exists(perm_name_participate)


@pytest.mark.django_db
def test_participate_project_draft(
    user_factory, group_factory, organisation, project_factory
):
    anonymous = AnonymousUser()
    user = user_factory()
    initiator = user_factory()
    moderator = user_factory()
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
    project = project_factory(group=group4, organisation=organisation, is_draft=True)
    project.moderators.add(moderator)

    assert not rules.has_perm(perm_name_participate, anonymous, project)
    assert not rules.has_perm(perm_name_participate, user, project)
    assert not rules.has_perm(perm_name_participate, group_member_in_orga, project)
    assert not rules.has_perm(perm_name_participate, group_member_out, project)
    assert rules.has_perm(perm_name_participate, group_member_in_project, project)
    assert rules.has_perm(perm_name_participate, moderator, project)
    assert rules.has_perm(perm_name_participate, initiator, project)
    assert rules.has_perm(perm_name_participate, admin, project)


@pytest.mark.django_db
def test_participate_live_project(
    user_factory, group_factory, organisation, project_factory
):
    anonymous = AnonymousUser()
    user = user_factory()
    initiator = user_factory()
    moderator = user_factory()
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
    project.moderators.add(moderator)

    assert rules.has_perm(perm_name_participate, anonymous, project)
    assert rules.has_perm(perm_name_participate, user, project)
    assert rules.has_perm(perm_name_participate, group_member_in_orga, project)
    assert rules.has_perm(perm_name_participate, group_member_out, project)
    assert rules.has_perm(perm_name_participate, group_member_in_project, project)
    assert rules.has_perm(perm_name_participate, moderator, project)
    assert rules.has_perm(perm_name_participate, initiator, project)
    assert rules.has_perm(perm_name_participate, admin, project)


@pytest.mark.django_db
def test_participate_archived_project(
    user_factory, group_factory, organisation, project_factory
):
    anonymous = AnonymousUser()
    user = user_factory()
    initiator = user_factory()
    moderator = user_factory()
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
    project = project_factory(group=group4, organisation=organisation, is_archived=True)
    project.moderators.add(moderator)

    assert rules.has_perm(perm_name_participate, anonymous, project)
    assert rules.has_perm(perm_name_participate, user, project)
    assert rules.has_perm(perm_name_participate, group_member_in_orga, project)
    assert rules.has_perm(perm_name_participate, group_member_out, project)
    assert rules.has_perm(perm_name_participate, group_member_in_project, project)
    assert rules.has_perm(perm_name_participate, moderator, project)
    assert rules.has_perm(perm_name_participate, initiator, project)
    assert rules.has_perm(perm_name_participate, admin, project)


@pytest.mark.django_db
def test_participate_private_project(
    user_factory, group_factory, organisation, project_factory
):
    anonymous = AnonymousUser()
    user = user_factory()
    participant = user_factory()
    initiator = user_factory()
    moderator = user_factory()
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
    project = project_factory(
        group=group4, organisation=organisation, access=Access.PRIVATE
    )
    project.moderators.add(moderator)
    project.participants.add(participant)

    assert project.access == Access.PRIVATE
    assert not rules.has_perm(perm_name_participate, anonymous, project)
    assert not rules.has_perm(perm_name_participate, user, project)
    assert not rules.has_perm(perm_name_participate, group_member_in_orga, project)
    assert not rules.has_perm(perm_name_participate, group_member_out, project)
    assert rules.has_perm(perm_name_participate, group_member_in_project, project)
    assert rules.has_perm(perm_name_participate, participant, project)
    assert rules.has_perm(perm_name_participate, moderator, project)
    assert rules.has_perm(perm_name_participate, initiator, project)
    assert rules.has_perm(perm_name_participate, admin, project)


@pytest.mark.django_db
def test_participate_semiprivate_project(
    user_factory, group_factory, organisation, project_factory
):
    anonymous = AnonymousUser()
    user = user_factory()
    participant = user_factory()
    initiator = user_factory()
    moderator = user_factory()
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
    project = project_factory(
        group=group4, organisation=organisation, access=Access.SEMIPUBLIC
    )
    project.moderators.add(moderator)
    project.participants.add(participant)

    assert project.access == Access.SEMIPUBLIC
    assert not rules.has_perm(perm_name_participate, anonymous, project)
    assert not rules.has_perm(perm_name_participate, user, project)
    assert not rules.has_perm(perm_name_participate, group_member_in_orga, project)
    assert not rules.has_perm(perm_name_participate, group_member_out, project)
    assert rules.has_perm(perm_name_participate, group_member_in_project, project)
    assert rules.has_perm(perm_name_participate, participant, project)
    assert rules.has_perm(perm_name_participate, moderator, project)
    assert rules.has_perm(perm_name_participate, initiator, project)
    assert rules.has_perm(perm_name_participate, admin, project)
