import pytest
import rules

from meinberlin.apps.polls import phases
from meinberlin.test.helpers import freeze_phase
from meinberlin.test.helpers import freeze_post_phase
from meinberlin.test.helpers import freeze_pre_phase
from meinberlin.test.helpers import setup_phase
from meinberlin.test.helpers import setup_users

perm_name = 'meinberlin_polls.add_vote'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_pre_phase(phase_factory, poll_factory, question, choice, vote, user):
    phase, module, project, _ = setup_phase(phase_factory, poll_factory,
                                            phases.VotingPhase)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_public
    with freeze_pre_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_phase_active(phase_factory, poll_factory, question, choice, vote,
                      user):
    phase, module, project, _ = setup_phase(phase_factory, poll_factory,
                                            phases.VotingPhase)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_public
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_phase_active_project_draft(phase_factory, poll_factory, question,
                                    choice, vote, user):
    phase, module, project, _ = setup_phase(phase_factory, poll_factory,
                                            phases.VotingPhase,
                                            module__project__is_draft=True)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_draft
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_post_phase_project_archived(phase_factory, poll_factory, question,
                                     choice, vote, user):
    phase, module, project, _ = setup_phase(phase_factory, poll_factory,
                                            phases.VotingPhase,
                                            module__project__is_archived=True)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_archived
    with freeze_post_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)
