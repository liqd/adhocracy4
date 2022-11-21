import pytest
import rules

from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import freeze_post_phase
from adhocracy4.test.helpers import freeze_pre_phase
from adhocracy4.test.helpers import setup_phase
from adhocracy4.test.helpers import setup_users
from meinberlin.apps.budgeting import phases
from meinberlin.test.helpers import setup_group_members

perm_name = 'meinberlin_budgeting.add_proposal'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_pre_phase(phase_factory, user, admin, user_factory, group_factory):
    phase, module, project, _ = setup_phase(phase_factory, None,
                                            phases.RequestPhase)
    anonymous, moderator, initiator = setup_users(project)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_group_members(project, group_factory, user_factory)

    assert project.access == Access.PUBLIC
    with freeze_pre_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, group_member_out, module)
        assert not rules.has_perm(perm_name, group_member_in_org, module)
        assert rules.has_perm(perm_name, group_member_in_pro, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)
        assert rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_request_phase_active(phase_factory, user, admin, user_factory,
                              group_factory):
    phase, module, project, _ = setup_phase(phase_factory, None,
                                            phases.RequestPhase)
    anonymous, moderator, initiator = setup_users(project)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_group_members(project, group_factory, user_factory)

    assert project.access == Access.PUBLIC
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, group_member_out, module)
        assert rules.has_perm(perm_name, group_member_in_org, module)
        assert rules.has_perm(perm_name, group_member_in_pro, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)
        assert rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_collect_phase_active(phase_factory, user, admin, user_factory,
                              group_factory):
    phase, module, project, _ = setup_phase(phase_factory, None,
                                            phases.CollectPhase)
    anonymous, moderator, initiator = setup_users(project)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_group_members(project, group_factory, user_factory)

    assert project.access == Access.PUBLIC
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, group_member_out, module)
        assert rules.has_perm(perm_name, group_member_in_org, module)
        assert rules.has_perm(perm_name, group_member_in_pro, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)
        assert rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_rating_phase_active(phase_factory, user, admin, user_factory,
                             group_factory):
    phase, module, project, _ = setup_phase(phase_factory, None,
                                            phases.RatingPhase)
    anonymous, moderator, initiator = setup_users(project)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_group_members(project, group_factory, user_factory)

    assert project.access == Access.PUBLIC
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, group_member_out, module)
        assert not rules.has_perm(perm_name, group_member_in_org, module)
        assert rules.has_perm(perm_name, group_member_in_pro, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)
        assert rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_phase_active_project_private(phase_factory, user, admin,
                                      user_factory, group_factory):
    phase, module, project, _ = setup_phase(
        phase_factory, None, phases.RequestPhase,
        module__project__access=Access.PRIVATE)
    anonymous, moderator, initiator = setup_users(project)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_group_members(project, group_factory, user_factory)

    participant = user_factory()
    project.participants.add(participant)

    assert project.access == Access.PRIVATE
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, group_member_out, module)
        assert not rules.has_perm(perm_name, group_member_in_org, module)
        assert rules.has_perm(perm_name, group_member_in_pro, module)
        assert rules.has_perm(perm_name, participant, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)
        assert rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_phase_active_project_semipublic(phase_factory, user, admin,
                                         user_factory, group_factory):
    phase, module, project, _ = setup_phase(
        phase_factory, None, phases.RequestPhase,
        module__project__access=Access.SEMIPUBLIC)
    anonymous, moderator, initiator = setup_users(project)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_group_members(project, group_factory, user_factory)

    participant = user_factory()
    project.participants.add(participant)

    assert project.access == Access.SEMIPUBLIC
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, group_member_out, module)
        assert not rules.has_perm(perm_name, group_member_in_org, module)
        assert rules.has_perm(perm_name, group_member_in_pro, module)
        assert rules.has_perm(perm_name, participant, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)
        assert rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_phase_active_project_draft(phase_factory, user, admin, user_factory,
                                    group_factory):
    phase, module, project, _ = setup_phase(phase_factory, None,
                                            phases.RequestPhase,
                                            module__project__is_draft=True)
    anonymous, moderator, initiator = setup_users(project)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_group_members(project, group_factory, user_factory)

    assert project.is_draft
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, group_member_out, module)
        assert not rules.has_perm(perm_name, group_member_in_org, module)
        assert rules.has_perm(perm_name, group_member_in_pro, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)
        assert rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_post_phase_project_archived(phase_factory, user, admin, user_factory,
                                     group_factory):
    phase, module, project, _ = setup_phase(phase_factory, None,
                                            phases.RequestPhase,
                                            module__project__is_archived=True)
    anonymous, moderator, initiator = setup_users(project)
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_group_members(project, group_factory, user_factory)

    assert project.is_archived
    with freeze_post_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, group_member_out, module)
        assert not rules.has_perm(perm_name, group_member_in_org, module)
        assert rules.has_perm(perm_name, group_member_in_pro, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)
        assert rules.has_perm(perm_name, admin, module)
