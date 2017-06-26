from datetime import timedelta

import pytest
import rules
from freezegun import freeze_time

from apps.ideas import phases
from tests.helpers import setup_phase
from tests.helpers import setup_users

perm_name = 'meinberlin_ideas.rate_idea'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_rules_pre_phase(phase_factory, idea_factory, user):
    phase, _, project, item = setup_phase(phase_factory, idea_factory,
                                          phases.CollectPhase)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_public
    with freeze_time(phase.start_date - timedelta(days=1)):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)


@pytest.mark.django_db
def test_rules_public(phase_factory, idea_factory, user):
    phase, _, project, item = setup_phase(phase_factory, idea_factory,
                                          phases.CollectPhase)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_public
    with freeze_time(phase.start_date + timedelta(seconds=1)):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)


@pytest.mark.django_db
def test_rules_draft(phase_factory, idea_factory, user):
    phase, _, project, item = setup_phase(phase_factory, idea_factory,
                                          phases.CollectPhase,
                                          module__project__is_draft=True)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_draft
    with freeze_time(phase.start_date + timedelta(seconds=1)):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)


@pytest.mark.django_db
def test_rules_archived(phase_factory, idea_factory, user):
    phase, _, project, item = setup_phase(phase_factory, idea_factory,
                                          phases.CollectPhase,
                                          module__project__is_archived=True)
    anonymous, moderator, initiator = setup_users(project)

    assert project.is_archived
    with freeze_time(phase.end_date + timedelta(seconds=1)):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)
