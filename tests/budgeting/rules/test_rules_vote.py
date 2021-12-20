import pytest
import rules

from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import freeze_post_phase
from adhocracy4.test.helpers import freeze_pre_phase
from adhocracy4.test.helpers import setup_phase
from adhocracy4.test.helpers import setup_users
from meinberlin.apps.budgeting import phases

perm_name = 'meinberlin_budgeting.vote_proposal'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


# This test is modeled on test_rules_rate.
# I guess the permissions aren't completely tested by testing the rules here
# b/c the existing rule only checks for the phase being active...
@pytest.mark.django_db
def test_pre_phase(user_factory, phase_factory, proposal_factory, user):
    phase, module, project, _ = setup_phase(phase_factory, proposal_factory,
                                            phases.RequestPhase)
    anonymous, moderator, initiator = setup_users(project)
    admin = user_factory(is_superuser=True)

    assert project.is_public
    with freeze_pre_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, moderator, module)
        assert not rules.has_perm(perm_name, initiator, module)
        assert not rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_request_phase_active(user_factory, phase_factory, proposal_factory,
                              user):
    phase, module, project, _ = setup_phase(phase_factory, proposal_factory,
                                            phases.RequestPhase)
    anonymous, moderator, initiator = setup_users(project)
    admin = user_factory(is_superuser=True)

    assert project.is_public
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, moderator, module)
        assert not rules.has_perm(perm_name, initiator, module)
        assert not rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_collect_phase_active(user_factory, phase_factory, proposal_factory,
                              user):
    phase, module, project, _ = setup_phase(phase_factory, proposal_factory,
                                            phases.CollectPhase)
    anonymous, moderator, initiator = setup_users(project)
    admin = user_factory(is_superuser=True)

    assert project.is_public
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, admin, module)
        assert not rules.has_perm(perm_name, moderator, module)
        assert not rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_rating_phase_active(user_factory, phase_factory, proposal_factory,
                             user):
    phase, module, project, _ = setup_phase(phase_factory, proposal_factory,
                                            phases.RatingPhase)
    anonymous, moderator, initiator = setup_users(project)
    admin = user_factory(is_superuser=True)

    assert project.is_public
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, admin, module)
        assert not rules.has_perm(perm_name, moderator, module)
        assert not rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_voting_phase_active(user_factory, phase_factory, proposal_factory,
                             user):
    phase, module, project, _ = setup_phase(phase_factory, proposal_factory,
                                            phases.VotingPhase)
    anonymous, moderator, initiator = setup_users(project)
    admin = user_factory(is_superuser=True)

    assert project.is_public
    with freeze_phase(phase):
        assert rules.has_perm(perm_name, anonymous, module)
        assert rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, admin, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_phase_active_project_private(user_factory, phase_factory,
                                      proposal_factory, user, user2):
    phase, module, project, _ = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase,
        module__project__access=Access.PRIVATE)
    anonymous, moderator, initiator = setup_users(project)
    admin = user_factory(is_superuser=True)

    participant = user2
    project.participants.add(participant)

    assert project.access == Access.PRIVATE
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, participant, module)
        assert not rules.has_perm(perm_name, moderator, module)
        assert not rules.has_perm(perm_name, initiator, module)
        assert not rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_phase_active_project_semipublic(user_factory, phase_factory,
                                         proposal_factory, user, user2):
    phase, module, project, _ = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase,
        module__project__access=Access.SEMIPUBLIC)
    anonymous, moderator, initiator = setup_users(project)
    admin = user_factory(is_superuser=True)

    participant = user2
    project.participants.add(participant)

    assert project.access == Access.SEMIPUBLIC
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, participant, module)
        assert not rules.has_perm(perm_name, moderator, module)
        assert not rules.has_perm(perm_name, initiator, module)
        assert not rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_phase_active_project_draft(user_factory, phase_factory,
                                    proposal_factory, user):
    phase, module, project, _ = setup_phase(phase_factory, proposal_factory,
                                            phases.RequestPhase,
                                            module__project__is_draft=True)
    anonymous, moderator, initiator = setup_users(project)
    admin = user_factory(is_superuser=True)

    assert project.is_draft
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, moderator, module)
        assert not rules.has_perm(perm_name, initiator, module)
        assert not rules.has_perm(perm_name, admin, module)


@pytest.mark.django_db
def test_post_phase_project_archived(user_factory, phase_factory,
                                     proposal_factory, user):
    phase, module, project, _ = setup_phase(phase_factory, proposal_factory,
                                            phases.RequestPhase,
                                            module__project__is_archived=True)
    anonymous, moderator, initiator = setup_users(project)
    admin = user_factory(is_superuser=True)

    assert project.is_archived
    with freeze_post_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, moderator, module)
        assert not rules.has_perm(perm_name, initiator, module)
        assert not rules.has_perm(perm_name, admin, module)
