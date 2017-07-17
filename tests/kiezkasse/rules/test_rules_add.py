import pytest
import rules

from apps.kiezkasse import phases
from tests.helpers import freeze_phase
from tests.helpers import freeze_post_phase
from tests.helpers import freeze_pre_phase
from tests.helpers import setup_phase
from tests.helpers import setup_users

perm_name = 'meinberlin_kiezkasse.add_proposal'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_pre_phase(phase_factory, user):
    phase, module, project, _ = setup_phase(phase_factory, None,
                                            phases.RequestPhase)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_public
    with freeze_pre_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_phase_active(phase_factory, user):
    phase, module, project, _ = setup_phase(phase_factory, None,
                                            phases.RequestPhase)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_public
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_phase_active_project_private(phase_factory, user, user2):
    phase, module, project, _ = setup_phase(phase_factory, None,
                                            phases.RequestPhase,
                                            module__project__is_public=False)
    anonymous, moderator, initiator = setup_users(project)

    participant = user2
    project.participants.add(participant)

    assert not project.is_public
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, participant, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_phase_active_project_draft(phase_factory, user):
    phase, module, project, _ = setup_phase(phase_factory, None,
                                            phases.RequestPhase,
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
                                            phases.RequestPhase,
                                            module__project__is_archived=True)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_archived
    with freeze_post_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)
