import pytest
import rules

from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import freeze_post_phase
from adhocracy4.test.helpers import freeze_pre_phase
from adhocracy4.test.helpers import setup_phase
from adhocracy4.test.helpers import setup_users
from meinberlin.apps.bplan import phases
from meinberlin.test.helpers import setup_multiple_group_members

perm_name = 'meinberlin_bplan.change_bplan'

# This permission is used in the API, not in the views.


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_pre_phase(phase_factory, user_factory, group_factory):
    phase, _, project, _ = setup_phase(phase_factory, None,
                                       phases.StatementPhase)
    anonymous, moderator, initiator = setup_users(project)
    user = user_factory()
    admin = user_factory(is_superuser=True)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_multiple_group_members(project, group_factory, user_factory)

    assert project.is_public
    with freeze_pre_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, project)
        assert not rules.has_perm(perm_name, user, project)
        assert not rules.has_perm(perm_name, group_member_out, project)
        assert not rules.has_perm(perm_name, group_member_in_org, project)
        assert not rules.has_perm(perm_name, group_member_in_pro, project)
        assert not rules.has_perm(perm_name, moderator, project)
        assert rules.has_perm(perm_name, initiator, project)
        assert not rules.has_perm(perm_name, admin, project)


@pytest.mark.django_db
def test_phase_active(phase_factory, user_factory, group_factory):
    phase, _, project, _ = setup_phase(phase_factory, None,
                                       phases.StatementPhase)
    anonymous, moderator, initiator = setup_users(project)
    user = user_factory()
    admin = user_factory(is_superuser=True)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_multiple_group_members(project, group_factory, user_factory)

    assert project.is_public
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, project)
        assert not rules.has_perm(perm_name, user, project)
        assert not rules.has_perm(perm_name, group_member_out, project)
        assert not rules.has_perm(perm_name, group_member_in_org, project)
        assert not rules.has_perm(perm_name, group_member_in_pro, project)
        assert not rules.has_perm(perm_name, moderator, project)
        assert rules.has_perm(perm_name, initiator, project)
        assert not rules.has_perm(perm_name, admin, project)


@pytest.mark.django_db
def test_phase_active_project_draft(phase_factory, user_factory,
                                    group_factory):
    phase, _, project, _ = setup_phase(phase_factory, None,
                                       phases.StatementPhase,
                                       module__project__is_draft=True)
    anonymous, moderator, initiator = setup_users(project)
    user = user_factory()
    admin = user_factory(is_superuser=True)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_multiple_group_members(project, group_factory, user_factory)

    assert project.is_draft
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, project)
        assert not rules.has_perm(perm_name, user, project)
        assert not rules.has_perm(perm_name, group_member_out, project)
        assert not rules.has_perm(perm_name, group_member_in_org, project)
        assert not rules.has_perm(perm_name, group_member_in_pro, project)
        assert not rules.has_perm(perm_name, moderator, project)
        assert rules.has_perm(perm_name, initiator, project)
        assert not rules.has_perm(perm_name, admin, project)


@pytest.mark.django_db
def test_post_phase_project_archived(phase_factory, user_factory,
                                     group_factory):
    phase, _, project, _ = setup_phase(phase_factory, None,
                                       phases.StatementPhase,
                                       module__project__is_archived=True)
    anonymous, moderator, initiator = setup_users(project)
    user = user_factory()
    admin = user_factory(is_superuser=True)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_multiple_group_members(project, group_factory, user_factory)

    assert project.is_archived
    with freeze_post_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, project)
        assert not rules.has_perm(perm_name, user, project)
        assert not rules.has_perm(perm_name, group_member_out, project)
        assert not rules.has_perm(perm_name, group_member_in_org, project)
        assert not rules.has_perm(perm_name, group_member_in_pro, project)
        assert not rules.has_perm(perm_name, moderator, project)
        assert rules.has_perm(perm_name, initiator, project)
        assert not rules.has_perm(perm_name, admin, project)
