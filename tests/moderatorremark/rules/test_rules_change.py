import pytest
import rules

from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import setup_users
from meinberlin.test.helpers import setup_group_members

perm_name = "meinberlin_moderatorremark.change_moderatorremark"


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_change(moderator_remark, user, admin, user_factory, group_factory):
    project = moderator_remark.item.module.project
    anonymous, moderator, initiator = setup_users(project)
    creator = moderator_remark.creator
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)

    assert project.is_public

    assert not rules.has_perm(perm_name, anonymous, moderator_remark)
    assert not rules.has_perm(perm_name, user, moderator_remark)
    assert not rules.has_perm(perm_name, creator, moderator_remark)
    assert not rules.has_perm(perm_name, group_member_out, moderator_remark)
    assert not rules.has_perm(perm_name, group_member_in_org, moderator_remark)
    assert rules.has_perm(perm_name, group_member_in_pro, moderator_remark)
    assert rules.has_perm(perm_name, moderator, moderator_remark)
    assert rules.has_perm(perm_name, initiator, moderator_remark)
    assert rules.has_perm(perm_name, admin, moderator_remark)


@pytest.mark.django_db
def test_change_private_project(
    moderator_remark, user, admin, user_factory, group_factory
):
    project = moderator_remark.item.module.project
    project.access = Access.PRIVATE
    project.save()

    participant = user_factory()
    project.participants.add(participant)
    anonymous, moderator, initiator = setup_users(project)
    creator = moderator_remark.creator
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)

    assert project.is_private

    assert not rules.has_perm(perm_name, anonymous, moderator_remark)
    assert not rules.has_perm(perm_name, user, moderator_remark)
    assert not rules.has_perm(perm_name, participant, moderator_remark)
    assert not rules.has_perm(perm_name, creator, moderator_remark)
    assert not rules.has_perm(perm_name, group_member_out, moderator_remark)
    assert not rules.has_perm(perm_name, group_member_in_org, moderator_remark)
    assert rules.has_perm(perm_name, group_member_in_pro, moderator_remark)
    assert rules.has_perm(perm_name, moderator, moderator_remark)
    assert rules.has_perm(perm_name, initiator, moderator_remark)
    assert rules.has_perm(perm_name, admin, moderator_remark)
