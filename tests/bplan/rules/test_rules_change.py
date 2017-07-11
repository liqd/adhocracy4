import pytest
import rules

from apps.bplan import phases
from tests.helpers import freeze_phase
from tests.helpers import freeze_post_phase
from tests.helpers import freeze_pre_phase
from tests.helpers import setup_phase
from tests.helpers import setup_users

perm_name = 'meinberlin_bplan.change_bplan'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_pre_phase(phase_factory, user):
    phase, _, project, _ = setup_phase(phase_factory, None,
                                       phases.StatementPhase)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_public
    with freeze_pre_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, project)
        assert not rules.has_perm(perm_name, user, project)
        assert not rules.has_perm(perm_name, moderator, project)
        assert rules.has_perm(perm_name, initiator, project)


@pytest.mark.django_db
def test_phase_active(phase_factory, user):
    phase, _, project, _ = setup_phase(phase_factory, None,
                                       phases.StatementPhase)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_public
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, project)
        assert not rules.has_perm(perm_name, user, project)
        assert not rules.has_perm(perm_name, moderator, project)
        assert rules.has_perm(perm_name, initiator, project)


@pytest.mark.django_db
def test_phase_active_project_draft(phase_factory, user):
    phase, _, project, _ = setup_phase(phase_factory, None,
                                       phases.StatementPhase,
                                       module__project__is_draft=True)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_draft
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, project)
        assert not rules.has_perm(perm_name, user, project)
        assert not rules.has_perm(perm_name, moderator, project)
        assert rules.has_perm(perm_name, initiator, project)


@pytest.mark.django_db
def test_post_phase_project_archived(phase_factory, user):
    phase, _, project, _ = setup_phase(phase_factory, None,
                                       phases.StatementPhase,
                                       module__project__is_archived=True)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_archived
    with freeze_post_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, project)
        assert not rules.has_perm(perm_name, user, project)
        assert not rules.has_perm(perm_name, moderator, project)
        assert rules.has_perm(perm_name, initiator, project)
