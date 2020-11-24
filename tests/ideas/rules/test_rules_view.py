import pytest
import rules

from adhocracy4.projects.enums import Access
from meinberlin.apps.ideas import phases
from meinberlin.test.helpers import freeze_phase
from meinberlin.test.helpers import freeze_post_phase
from meinberlin.test.helpers import freeze_pre_phase
from meinberlin.test.helpers import setup_phase
from meinberlin.test.helpers import setup_users

perm_name = 'meinberlin_ideas.view_idea'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_pre_phase(phase_factory, idea_factory, user):
    phase, _, project, item = setup_phase(phase_factory, idea_factory,
                                          phases.CollectPhase)
    anonymous, moderator, initiator = setup_users(project)

    assert project.access == Access.PUBLIC
    with freeze_pre_phase(phase):
        assert rules.has_perm(perm_name, anonymous, item)
        assert rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)


@pytest.mark.django_db
def test_phase_active(phase_factory, idea_factory, user):
    phase, _, project, item = setup_phase(phase_factory, idea_factory,
                                          phases.CollectPhase)
    anonymous, moderator, initiator = setup_users(project)

    assert project.access == Access.PUBLIC
    with freeze_phase(phase):
        assert rules.has_perm(perm_name, anonymous, item)
        assert rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)


@pytest.mark.django_db
def test_phase_active_project_private(phase_factory, idea_factory,
                                      user, user2):
    phase, _, project, item = setup_phase(
        phase_factory, idea_factory, phases.CollectPhase,
        module__project__access=Access.PRIVATE)
    anonymous, moderator, initiator = setup_users(project)
    participant = user2
    project.participants.add(participant)

    assert project.access == Access.PRIVATE
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, participant, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)


@pytest.mark.django_db
def test_phase_active_project_draft(phase_factory, idea_factory, user):
    phase, _, project, item = setup_phase(phase_factory, idea_factory,
                                          phases.CollectPhase,
                                          module__project__is_draft=True)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_draft
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)


@pytest.mark.django_db
def test_post_phase_project_archived(phase_factory, idea_factory, user):
    phase, _, project, item = setup_phase(phase_factory, idea_factory,
                                          phases.CollectPhase,
                                          module__project__is_archived=True)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_archived
    with freeze_post_phase(phase):
        assert rules.has_perm(perm_name, anonymous, item)
        assert rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)
