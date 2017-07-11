import pytest
import rules

from apps.polls import phases
from tests.helpers import freeze_phase
from tests.helpers import freeze_post_phase
from tests.helpers import freeze_pre_phase
from tests.helpers import setup_phase
from tests.helpers import setup_users
from tests.polls.helpers import setup_poll

perm_name = 'meinberlin_polls.add_vote'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_pre_phase(phase_factory, poll_factory, question, choice, vote, user):
    phase, _, project, item = setup_phase(phase_factory, poll_factory,
                                          phases.VotingPhase)
    anonymous, moderator, initiator = setup_users(project)
    setup_poll(item, question, choice, vote)
    creator = item.creator

    assert project.is_public
    with freeze_pre_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, vote)
        assert not rules.has_perm(perm_name, user, vote)
        assert not rules.has_perm(perm_name, creator, vote)
        assert rules.has_perm(perm_name, moderator, vote)
        assert rules.has_perm(perm_name, initiator, vote)


@pytest.mark.django_db
def test_phase_active(phase_factory, poll_factory, question, choice, vote,
                      user):
    phase, _, project, item = setup_phase(phase_factory, poll_factory,
                                          phases.VotingPhase)
    anonymous, moderator, initiator = setup_users(project)
    setup_poll(item, question, choice, vote)
    creator = item.creator

    assert project.is_public
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, vote)
        assert rules.has_perm(perm_name, user, vote)
        assert rules.has_perm(perm_name, creator, vote)
        assert rules.has_perm(perm_name, moderator, vote)
        assert rules.has_perm(perm_name, initiator, vote)


@pytest.mark.django_db
def test_phase_active_project_draft(phase_factory, poll_factory, question,
                                    choice, vote, user):
    phase, _, project, item = setup_phase(phase_factory, poll_factory,
                                          phases.VotingPhase,
                                          module__project__is_draft=True)
    anonymous, moderator, initiator = setup_users(project)
    setup_poll(item, question, choice, vote)
    creator = item.creator

    assert project.is_draft
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, vote)
        assert not rules.has_perm(perm_name, user, vote)
        assert not rules.has_perm(perm_name, creator, vote)
        assert rules.has_perm(perm_name, moderator, vote)
        assert rules.has_perm(perm_name, initiator, vote)


@pytest.mark.django_db
def test_post_phase_project_archived(phase_factory, poll_factory, question,
                                     choice, vote, user):
    phase, _, project, item = setup_phase(phase_factory, poll_factory,
                                          phases.VotingPhase,
                                          module__project__is_archived=True)
    anonymous, moderator, initiator = setup_users(project)
    setup_poll(item, question, choice, vote)
    creator = item.creator

    assert project.is_archived
    with freeze_post_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, vote)
        assert not rules.has_perm(perm_name, user, vote)
        assert not rules.has_perm(perm_name, creator, vote)
        assert rules.has_perm(perm_name, moderator, vote)
        assert rules.has_perm(perm_name, initiator, vote)
