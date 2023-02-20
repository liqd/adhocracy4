from datetime import timedelta

import pytest
import rules
from freezegun import freeze_time

from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import freeze_post_phase
from adhocracy4.test.helpers import freeze_pre_phase
from adhocracy4.test.helpers import setup_phase
from adhocracy4.test.helpers import setup_users
from meinberlin.apps.budgeting import phases
from meinberlin.test.helpers import setup_group_members

perm_name = "meinberlin_budgeting.view_vote_count"


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_module_no_voting_phase(
    phase_factory, proposal_factory, user, admin, user_factory, group_factory
):
    collect_phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.CollectPhase
    )
    anonymous, moderator, initiator = setup_users(project)
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)

    assert project.is_public
    with freeze_phase(collect_phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, group_member_out, module)
        assert not rules.has_perm(perm_name, group_member_in_org, module)
        assert not rules.has_perm(perm_name, group_member_in_pro, module)
        assert not rules.has_perm(perm_name, moderator, module)
        assert not rules.has_perm(perm_name, initiator, module)
        assert not rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_pre_phase(
    phase_factory, proposal_factory, user, admin, user_factory, group_factory
):
    collect_phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.CollectPhase
    )
    phase_factory(
        phase_content=phases.VotingPhase,
        module=module,
        start_date=collect_phase.end_date + timedelta(hours=2),
        end_date=collect_phase.end_date + timedelta(hours=3),
        type="meinberlin_budgeting:voting",
    )
    anonymous, moderator, initiator = setup_users(project)
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)

    assert project.is_public
    with freeze_pre_phase(collect_phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, group_member_out, module)
        assert not rules.has_perm(perm_name, group_member_in_org, module)
        assert not rules.has_perm(perm_name, group_member_in_pro, module)
        assert not rules.has_perm(perm_name, moderator, module)
        assert not rules.has_perm(perm_name, initiator, module)
        assert rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_support_phase_active(
    phase_factory, proposal_factory, user, admin, user_factory, group_factory
):
    support_phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.SupportPhase
    )
    phase_factory(
        phase_content=phases.VotingPhase,
        module=module,
        start_date=support_phase.end_date + timedelta(hours=2),
        end_date=support_phase.end_date + timedelta(hours=3),
        type="meinberlin_budgeting:voting",
    )

    anonymous, moderator, initiator = setup_users(project)
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)

    assert project.is_public
    with freeze_phase(support_phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, group_member_out, module)
        assert not rules.has_perm(perm_name, group_member_in_org, module)
        assert not rules.has_perm(perm_name, group_member_in_pro, module)
        assert not rules.has_perm(perm_name, moderator, module)
        assert not rules.has_perm(perm_name, initiator, module)
        assert rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_between_support_and_voting_phase(
    phase_factory, proposal_factory, user, admin, user_factory, group_factory
):
    support_phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.SupportPhase
    )
    phase_factory(
        phase_content=phases.VotingPhase,
        module=module,
        start_date=support_phase.end_date + timedelta(hours=2),
        end_date=support_phase.end_date + timedelta(hours=3),
        type="meinberlin_budgeting:voting",
    )
    between_phases = support_phase.end_date + timedelta(hours=1)

    anonymous, moderator, initiator = setup_users(project)
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)

    assert project.is_public
    with freeze_time(between_phases):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, group_member_out, module)
        assert not rules.has_perm(perm_name, group_member_in_org, module)
        assert not rules.has_perm(perm_name, group_member_in_pro, module)
        assert not rules.has_perm(perm_name, moderator, module)
        assert not rules.has_perm(perm_name, initiator, module)
        assert rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_voting_phase_active(
    phase_factory, proposal_factory, user, admin, user_factory, group_factory
):
    voting_phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    anonymous, moderator, initiator = setup_users(project)
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)

    assert project.is_public
    with freeze_phase(voting_phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, group_member_out, module)
        assert not rules.has_perm(perm_name, group_member_in_org, module)
        assert not rules.has_perm(perm_name, group_member_in_pro, module)
        assert not rules.has_perm(perm_name, moderator, module)
        assert not rules.has_perm(perm_name, initiator, module)
        assert rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_voting_phase_over(
    phase_factory, proposal_factory, user, admin, user_factory, group_factory
):
    voting_phase, module, project, item = setup_phase(
        phase_factory,
        proposal_factory,
        phases.VotingPhase,
    )
    anonymous, moderator, initiator = setup_users(project)
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)

    with freeze_post_phase(voting_phase):
        assert rules.has_perm(perm_name, anonymous, module)
        assert rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, group_member_out, module)
        assert rules.has_perm(perm_name, group_member_in_org, module)
        assert rules.has_perm(perm_name, group_member_in_pro, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)
        assert rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_voting_phase_over_project_private(
    phase_factory, proposal_factory, user, admin, user_factory, group_factory
):
    voting_phase, module, project, item = setup_phase(
        phase_factory,
        proposal_factory,
        phases.VotingPhase,
        module__project__access=Access.PRIVATE,
    )
    anonymous, moderator, initiator = setup_users(project)
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)

    participant = user_factory()
    project.participants.add(participant)

    assert project.access == Access.PRIVATE
    with freeze_post_phase(voting_phase):
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
def test_voting_phase_over_project_semipublic(
    phase_factory, proposal_factory, user, admin, user_factory, group_factory
):
    voting_phase, module, project, item = setup_phase(
        phase_factory,
        proposal_factory,
        phases.VotingPhase,
        module__project__access=Access.SEMIPUBLIC,
    )
    anonymous, moderator, initiator = setup_users(project)
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)

    participant = user_factory()
    project.participants.add(participant)

    assert project.access == Access.SEMIPUBLIC
    with freeze_post_phase(voting_phase):
        assert rules.has_perm(perm_name, anonymous, module)
        assert rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, group_member_out, module)
        assert rules.has_perm(perm_name, group_member_in_org, module)
        assert rules.has_perm(perm_name, group_member_in_pro, module)
        assert rules.has_perm(perm_name, participant, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)
        assert rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_voting_phase_over_project_draft(
    phase_factory, proposal_factory, user, admin, user_factory, group_factory
):
    voting_phase, module, project, item = setup_phase(
        phase_factory,
        proposal_factory,
        phases.VotingPhase,
        module__project__is_draft=True,
    )
    anonymous, moderator, initiator = setup_users(project)
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)

    assert project.is_draft
    with freeze_phase(voting_phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, group_member_out, module)
        assert not rules.has_perm(perm_name, group_member_in_org, module)
        assert not rules.has_perm(perm_name, group_member_in_pro, module)
        assert not rules.has_perm(perm_name, moderator, module)
        assert not rules.has_perm(perm_name, initiator, module)
        assert rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_post_phase_project_archived(
    phase_factory, proposal_factory, user, admin, user_factory, group_factory
):
    voting_phase, module, project, item = setup_phase(
        phase_factory,
        proposal_factory,
        phases.VotingPhase,
        module__project__is_archived=True,
    )
    anonymous, moderator, initiator = setup_users(project)
    (
        project,
        group_member_in_org,
        group_member_in_pro,
        group_member_out,
    ) = setup_group_members(project, group_factory, user_factory)

    assert project.is_archived
    with freeze_post_phase(voting_phase):
        assert rules.has_perm(perm_name, anonymous, module)
        assert rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, group_member_out, module)
        assert rules.has_perm(perm_name, group_member_in_org, module)
        assert rules.has_perm(perm_name, group_member_in_pro, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)
        assert rules.has_perm(perm_name, admin, module)
