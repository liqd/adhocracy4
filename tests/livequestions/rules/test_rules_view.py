import pytest
import rules

from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import freeze_post_phase
from adhocracy4.test.helpers import freeze_pre_phase
from adhocracy4.test.helpers import setup_phase
from adhocracy4.test.helpers import setup_users
from meinberlin.apps.livequestions import phases
from meinberlin.test.helpers import setup_group_members

perm_name = "meinberlin_livequestions.view_livequestion"


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_pre_phase(
    phase_factory, live_question_factory, user, admin, user_factory, group_factory
):
    phase, _, project, item = setup_phase(
        phase_factory, live_question_factory, phases.IssuePhase
    )
    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)

    assert project.access == Access.PUBLIC
    with freeze_pre_phase(phase):
        assert rules.has_perm(perm_name, anonymous, item)
        assert rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, creator, item)
        assert rules.has_perm(perm_name, group_member_out, item)
        assert rules.has_perm(perm_name, group_member_in_org, item)
        assert rules.has_perm(perm_name, group_member_in_pro, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)
        assert rules.has_perm(perm_name, admin, item)


@pytest.mark.django_db
def test_phase_active(
    phase_factory, live_question_factory, user, admin, user_factory, group_factory
):
    phase, _, project, item = setup_phase(
        phase_factory, live_question_factory, phases.IssuePhase
    )
    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)

    assert project.access == Access.PUBLIC
    with freeze_phase(phase):
        assert rules.has_perm(perm_name, anonymous, item)
        assert rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, creator, item)
        assert rules.has_perm(perm_name, group_member_out, item)
        assert rules.has_perm(perm_name, group_member_in_org, item)
        assert rules.has_perm(perm_name, group_member_in_pro, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)
        assert rules.has_perm(perm_name, admin, item)


@pytest.mark.django_db
def test_phase_active_project_private(
    phase_factory, live_question_factory, user, admin, user_factory, group_factory
):
    phase, _, project, item = setup_phase(
        phase_factory,
        live_question_factory,
        phases.IssuePhase,
        module__project__access=Access.PRIVATE,
    )
    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)
    participant = user_factory()
    project.participants.add(participant)

    assert project.access == Access.PRIVATE
    with freeze_phase(phase):
        assert rules.has_perm(perm_name, anonymous, item)
        assert rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, participant, item)
        assert rules.has_perm(perm_name, creator, item)
        assert rules.has_perm(perm_name, group_member_out, item)
        assert rules.has_perm(perm_name, group_member_in_org, item)
        assert rules.has_perm(perm_name, group_member_in_pro, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)
        assert rules.has_perm(perm_name, admin, item)


@pytest.mark.django_db
def test_phase_active_project_semipublic(
    phase_factory, live_question_factory, user, admin, user_factory, group_factory
):
    phase, _, project, item = setup_phase(
        phase_factory,
        live_question_factory,
        phases.IssuePhase,
        module__project__access=Access.SEMIPUBLIC,
    )
    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)
    participant = user_factory()
    project.participants.add(participant)

    assert project.access == Access.SEMIPUBLIC
    with freeze_phase(phase):
        assert rules.has_perm(perm_name, anonymous, item)
        assert rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, participant, item)
        assert rules.has_perm(perm_name, creator, item)
        assert rules.has_perm(perm_name, group_member_out, item)
        assert rules.has_perm(perm_name, group_member_in_org, item)
        assert rules.has_perm(perm_name, group_member_in_pro, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)
        assert rules.has_perm(perm_name, admin, item)


@pytest.mark.django_db
def test_post_phase_project_archived(
    phase_factory, live_question_factory, user, admin, user_factory, group_factory
):
    phase, _, project, item = setup_phase(
        phase_factory,
        live_question_factory,
        phases.IssuePhase,
        module__project__is_archived=True,
    )
    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)

    assert project.is_archived
    with freeze_post_phase(phase):
        assert rules.has_perm(perm_name, anonymous, item)
        assert rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, creator, item)
        assert rules.has_perm(perm_name, group_member_out, item)
        assert rules.has_perm(perm_name, group_member_in_org, item)
        assert rules.has_perm(perm_name, group_member_in_pro, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)
        assert rules.has_perm(perm_name, admin, item)
