import pytest
import rules

from adhocracy4.projects.enums import Access
from meinberlin.apps.topicprio import phases
from meinberlin.test.helpers import freeze_phase
from meinberlin.test.helpers import freeze_post_phase
from meinberlin.test.helpers import freeze_pre_phase
from meinberlin.test.helpers import setup_phase
from meinberlin.test.helpers import setup_users

perm_name = 'meinberlin_topicprio.add_topic'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_pre_phase(phase_factory, user):
    phase, module, project, _ = setup_phase(phase_factory, None,
                                            phases.PrioritizePhase)
    anonymous, moderator, initiator = setup_users(project)

    assert project.access == Access.PUBLIC
    with freeze_pre_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_phase_active(phase_factory, user):
    phase, module, project, _ = setup_phase(phase_factory, None,
                                            phases.PrioritizePhase)
    anonymous, moderator, initiator = setup_users(project)

    assert project.access == Access.PUBLIC
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_phase_active_project_private(phase_factory, user, user2):
    phase, module, project, _ = setup_phase(
        phase_factory, None, phases.PrioritizePhase,
        module__project__access=Access.PRIVATE)
    anonymous, moderator, initiator = setup_users(project)

    participant = user2
    project.participants.add(participant)

    assert project.access == Access.PRIVATE
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, participant, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_phase_active_project_semipublic(phase_factory, user, user2):
    phase, module, project, _ = setup_phase(
        phase_factory, None, phases.PrioritizePhase,
        module__project__access=Access.SEMIPUBLIC)
    anonymous, moderator, initiator = setup_users(project)

    participant = user2
    project.participants.add(participant)

    assert project.access == Access.SEMIPUBLIC
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert not rules.has_perm(perm_name, participant, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_phase_active_project_draft(phase_factory, user):
    phase, module, project, _ = setup_phase(phase_factory, None,
                                            phases.PrioritizePhase,
                                            module__project__is_draft=True)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_draft
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_post_phase_project_archived(phase_factory, user):
    phase, module, project, _ = setup_phase(phase_factory, None,
                                            phases.PrioritizePhase,
                                            module__project__is_archived=True)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_archived
    with freeze_post_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)
