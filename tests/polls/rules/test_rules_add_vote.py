import pytest
import rules

from adhocracy4.polls import phases
from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import freeze_post_phase
from adhocracy4.test.helpers import freeze_pre_phase
from adhocracy4.test.helpers import setup_phase
from adhocracy4.test.helpers import setup_users

perm_name = 'a4polls.add_vote'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_pre_phase(phase_factory, poll_factory, question, choice, vote,
                   user, user_factory):
    phase, module, project, _ = setup_phase(phase_factory, poll_factory,
                                            phases.VotingPhase)
    anonymous, moderator, _ = setup_users(project)
    initiator = user_factory()
    project.organisation.initiators.add(initiator)

    assert project.is_public
    with freeze_pre_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_phase_active(phase_factory, poll_factory, question, choice, vote,
                      user, user_factory):
    phase, module, project, _ = setup_phase(phase_factory, poll_factory,
                                            phases.VotingPhase)
    anonymous, moderator, _ = setup_users(project)
    initiator = user_factory()
    project.organisation.initiators.add(initiator)

    assert project.is_public
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_phase_active_project_private(phase_factory, poll_factory, question,
                                      choice, vote, user, another_user,
                                      user_factory):
    phase, module, project, _ = setup_phase(
        phase_factory, poll_factory, phases.VotingPhase,
        module__project__access=Access.PRIVATE)
    anonymous, moderator, _ = setup_users(project)
    initiator = user_factory()
    project.organisation.initiators.add(initiator)
    participant = another_user
    project.participants.add(participant)

    assert project.access == Access.PRIVATE
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, participant, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_phase_active_project_semipublic(phase_factory, poll_factory, question,
                                         choice, vote, user, another_user,
                                         user_factory):
    phase, module, project, _ = setup_phase(
        phase_factory, poll_factory, phases.VotingPhase,
        module__project__access=Access.SEMIPUBLIC)
    anonymous, moderator, _ = setup_users(project)
    initiator = user_factory()
    project.organisation.initiators.add(initiator)
    participant = another_user
    project.participants.add(participant)

    assert project.access == Access.SEMIPUBLIC
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, participant, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_phase_active_project_draft(phase_factory, poll_factory, question,
                                    choice, vote, user, user_factory):
    phase, module, project, _ = setup_phase(phase_factory, poll_factory,
                                            phases.VotingPhase,
                                            module__project__is_draft=True)
    anonymous, moderator, _ = setup_users(project)
    initiator = user_factory()
    project.organisation.initiators.add(initiator)

    assert project.is_draft
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_post_phase_project_archived(phase_factory, poll_factory, question,
                                     choice, vote, user, user_factory):
    phase, module, project, _ = setup_phase(phase_factory, poll_factory,
                                            phases.VotingPhase,
                                            module__project__is_archived=True)
    anonymous, moderator, _ = setup_users(project)
    initiator = user_factory()
    project.organisation.initiators.add(initiator)

    assert project.is_archived
    with freeze_post_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)
