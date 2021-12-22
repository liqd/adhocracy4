import pytest
import rules

from adhocracy4.test.helpers import setup_users
from tests.helpers import setup_group_users

perm_name = 'meinberlin_offlineevents.view_offlineevent'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_rule(offline_event, user_factory, group_factory,
              user):

    project = offline_event.project

    anonymous, moderator, initiator = setup_users(project)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    assert rules.has_perm(perm_name, anonymous, offline_event)
    assert rules.has_perm(perm_name, user, offline_event)
    assert rules.has_perm(perm_name, moderator, offline_event)
    assert rules.has_perm(perm_name, initiator, offline_event)
    assert rules.has_perm(perm_name, group_member_in_orga, offline_event)
    assert rules.has_perm(perm_name, group_member_out, offline_event)
    assert rules.has_perm(perm_name, group_member_in_project, offline_event)


@pytest.mark.django_db
def test_rule_project_draft(offline_event_factory, user_factory, group_factory,
                            user):

    offline_event = offline_event_factory(project__is_draft=True)
    project = offline_event.project

    anonymous, moderator, initiator = setup_users(project)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    assert project.is_draft
    assert not rules.has_perm(perm_name, anonymous, offline_event)
    assert not rules.has_perm(perm_name, user, offline_event)
    assert not rules.has_perm(perm_name, group_member_in_orga, offline_event)
    assert not rules.has_perm(perm_name, group_member_out, offline_event)
    assert rules.has_perm(perm_name, group_member_in_project, offline_event)
    assert rules.has_perm(perm_name, moderator, offline_event)
    assert rules.has_perm(perm_name, initiator, offline_event)


@pytest.mark.django_db
def test_rule_project_archived(offline_event_factory, user_factory,
                               group_factory, user):

    offline_event = offline_event_factory(project__is_archived=True)
    project = offline_event.project

    anonymous, moderator, initiator = setup_users(project)
    group_member_in_orga, group_member_out, group_member_in_project, project \
        = setup_group_users(user_factory, group_factory, project)

    assert project.is_archived
    assert rules.has_perm(perm_name, anonymous, offline_event)
    assert rules.has_perm(perm_name, user, offline_event)
    assert rules.has_perm(perm_name, group_member_in_orga, offline_event)
    assert rules.has_perm(perm_name, group_member_out, offline_event)
    assert rules.has_perm(perm_name, group_member_in_project, offline_event)
    assert rules.has_perm(perm_name, moderator, offline_event)
    assert rules.has_perm(perm_name, initiator, offline_event)
