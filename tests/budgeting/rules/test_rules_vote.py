import pytest
import rules

from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import freeze_post_phase
from adhocracy4.test.helpers import freeze_pre_phase
from adhocracy4.test.helpers import setup_phase
from adhocracy4.test.helpers import setup_users
from meinberlin.apps.budgeting import phases
from meinberlin.test.helpers import setup_multiple_group_members

perm_name = 'meinberlin_budgeting.vote_proposal'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


# This test is modeled on test_rules_rate.
# I guess the permissions aren't completely tested by testing the rules here
# b/c the existing rule only checks for the phase being active...
@pytest.mark.django_db
def test_pre_phase(
        user_factory, phase_factory, proposal_factory, user, admin,
        group_factory):
    phase, _, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase)
    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_multiple_group_members(project, group_factory, user_factory)

    assert project.is_public
    with freeze_pre_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert not rules.has_perm(perm_name, creator, item)
        assert not rules.has_perm(perm_name, group_member_out, item)
        assert not rules.has_perm(perm_name, group_member_in_org, item)
        assert not rules.has_perm(perm_name, group_member_in_pro, item)
        assert not rules.has_perm(perm_name, moderator, item)
        assert not rules.has_perm(perm_name, initiator, item)
        assert rules.has_perm(perm_name, admin, item)


@pytest.mark.django_db
def test_request_phase_active(
        user_factory, phase_factory, proposal_factory, user, admin,
        group_factory):
    phase, _, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase)
    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_multiple_group_members(project, group_factory, user_factory)

    assert project.is_public
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert not rules.has_perm(perm_name, creator, item)
        assert not rules.has_perm(perm_name, group_member_out, item)
        assert not rules.has_perm(perm_name, group_member_in_org, item)
        assert not rules.has_perm(perm_name, group_member_in_pro, item)
        assert not rules.has_perm(perm_name, moderator, item)
        assert not rules.has_perm(perm_name, initiator, item)
        assert rules.has_perm(perm_name, admin, item)


@pytest.mark.django_db
def test_collect_phase_active(
        user_factory, phase_factory, proposal_factory, user, admin,
        group_factory):
    phase, _, project, item = setup_phase(
        phase_factory, proposal_factory, phases.CollectPhase)
    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_multiple_group_members(project, group_factory, user_factory)

    assert project.is_public
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert not rules.has_perm(perm_name, creator, item)
        assert not rules.has_perm(perm_name, group_member_out, item)
        assert not rules.has_perm(perm_name, group_member_in_org, item)
        assert not rules.has_perm(perm_name, group_member_in_pro, item)
        assert not rules.has_perm(perm_name, moderator, item)
        assert not rules.has_perm(perm_name, initiator, item)
        assert rules.has_perm(perm_name, admin, item)


@pytest.mark.django_db
def test_rating_phase_active(
        user_factory, phase_factory, proposal_factory, user, admin,
        group_factory):
    phase, _, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RatingPhase)
    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_multiple_group_members(project, group_factory, user_factory)

    assert project.is_public
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert not rules.has_perm(perm_name, creator, item)
        assert not rules.has_perm(perm_name, group_member_out, item)
        assert not rules.has_perm(perm_name, group_member_in_org, item)
        assert not rules.has_perm(perm_name, group_member_in_pro, item)
        assert not rules.has_perm(perm_name, moderator, item)
        assert not rules.has_perm(perm_name, initiator, item)
        assert rules.has_perm(perm_name, admin, item)


@pytest.mark.django_db
def test_voting_phase_active(
        user_factory, phase_factory, proposal_factory, user, admin,
        group_factory):
    phase, _, project, item = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase)
    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_multiple_group_members(project, group_factory, user_factory)

    assert project.is_public
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
        user_factory, phase_factory, proposal_factory, user, admin,
        group_factory):
    phase, _, project, item = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase,
        module__project__access=Access.PRIVATE)
    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_multiple_group_members(project, group_factory, user_factory)

    participant = user_factory()
    project.participants.add(participant)

    assert project.access == Access.PRIVATE
    with freeze_phase(phase):
        assert rules.has_perm(perm_name, anonymous, item)
        assert rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, creator, item)
        assert rules.has_perm(perm_name, participant, item)
        assert rules.has_perm(perm_name, group_member_out, item)
        assert rules.has_perm(perm_name, group_member_in_org, item)
        assert rules.has_perm(perm_name, group_member_in_pro, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)
        assert rules.has_perm(perm_name, admin, item)


@pytest.mark.django_db
def test_phase_active_project_semipublic(
        user_factory, phase_factory, proposal_factory, user, admin,
        group_factory):
    phase, _, project, item = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase,
        module__project__access=Access.SEMIPUBLIC)
    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_multiple_group_members(project, group_factory, user_factory)

    participant = user_factory()
    project.participants.add(participant)

    assert project.access == Access.SEMIPUBLIC
    with freeze_phase(phase):
        assert rules.has_perm(perm_name, anonymous, item)
        assert rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, creator, item)
        assert rules.has_perm(perm_name, group_member_out, item)
        assert rules.has_perm(perm_name, group_member_in_org, item)
        assert rules.has_perm(perm_name, group_member_in_pro, item)
        assert rules.has_perm(perm_name, participant, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)
        assert rules.has_perm(perm_name, admin, item)


@pytest.mark.django_db
def test_phase_active_project_draft(
        user_factory, phase_factory, proposal_factory, user, admin,
        group_factory):
    phase, _, project, item = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase,
        module__project__is_draft=True)
    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_multiple_group_members(project, group_factory, user_factory)

    assert project.is_draft
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert not rules.has_perm(perm_name, creator, item)
        assert not rules.has_perm(perm_name, group_member_out, item)
        assert not rules.has_perm(perm_name, group_member_in_org, item)
        assert not rules.has_perm(perm_name, group_member_in_pro, item)
        assert not rules.has_perm(perm_name, moderator, item)
        assert not rules.has_perm(perm_name, initiator, item)
        assert rules.has_perm(perm_name, admin, item)


@pytest.mark.django_db
def test_post_phase_project_archived(
        user_factory, phase_factory, proposal_factory, user, admin,
        group_factory):
    phase, _, project, item = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase,
        module__project__is_archived=True)
    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_multiple_group_members(project, group_factory, user_factory)

    assert project.is_archived
    with freeze_post_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert not rules.has_perm(perm_name, creator, item)
        assert not rules.has_perm(perm_name, group_member_out, item)
        assert not rules.has_perm(perm_name, group_member_in_org, item)
        assert not rules.has_perm(perm_name, group_member_in_pro, item)
        assert not rules.has_perm(perm_name, moderator, item)
        assert not rules.has_perm(perm_name, initiator, item)
        assert rules.has_perm(perm_name, admin, item)


@pytest.mark.django_db
def test_phase_active_proposal_archived(
        user_factory, phase_factory, proposal_factory, user, admin,
        group_factory):
    phase, _, project, item = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase,
        module__project__is_draft=True)

    item.is_archived = True
    item.save()

    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator
    project, group_member_in_org, group_member_in_pro, group_member_out = \
        setup_multiple_group_members(project, group_factory, user_factory)

    assert project.is_draft
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert not rules.has_perm(perm_name, creator, item)
        assert not rules.has_perm(perm_name, group_member_out, item)
        assert not rules.has_perm(perm_name, group_member_in_org, item)
        assert not rules.has_perm(perm_name, group_member_in_pro, item)
        assert not rules.has_perm(perm_name, moderator, item)
        assert not rules.has_perm(perm_name, initiator, item)
        assert rules.has_perm(perm_name, admin, item)
