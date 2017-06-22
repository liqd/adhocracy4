from datetime import timedelta

import pytest
import rules
from django.contrib.auth.models import AnonymousUser
from freezegun import freeze_time

from apps.ideas import phases

perm_name = 'meinberlin_ideas.add_idea'


@pytest.mark.django_db
def test_rules_pre_phase(phase_factory, user):
    assert rules.perm_exists(perm_name)

    phase_content = phases.CollectPhase()
    phase = phase_factory(phase_content=phase_content)
    module = phase.module
    project = phase.module.project
    # TODO: what to do with the other phases that are not used?

    anonymous = AnonymousUser()
    moderator = project.moderators.first()
    initiator = project.organisation.initiators.first()

    assert project.is_public
    with freeze_time(phase.start_date - timedelta(days=1)):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_rules_public(phase_factory, user):
    assert rules.perm_exists(perm_name)

    phase_content = phases.CollectPhase()
    phase = phase_factory(phase_content=phase_content)
    module = phase.module
    project = phase.module.project
    # TODO: what to do with the other phases that are not used?

    anonymous = AnonymousUser()
    moderator = project.moderators.first()
    initiator = project.organisation.initiators.first()

    assert project.is_public
    with freeze_time(phase.start_date + timedelta(seconds=1)):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_rules_private(phase_factory, user, user2):
    assert rules.perm_exists(perm_name)

    phase_content = phases.CollectPhase()
    phase = phase_factory(phase_content=phase_content,
                          module__project__is_public=False)
    module = phase.module
    project = phase.module.project
    # TODO: what to do with the other phases that are not used?

    anonymous = AnonymousUser()
    moderator = project.moderators.first()
    initiator = project.organisation.initiators.first()
    participant = user2
    project.participants.add(participant)

    assert not project.is_public
    with freeze_time(phase.start_date + timedelta(seconds=1)):
        assert not rules.has_perm(perm_name, anonymous, module)
        assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, participant, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_rules_draft(phase_factory, user):
    assert rules.perm_exists(perm_name)

    phase_content = phases.CollectPhase()
    phase = phase_factory(phase_content=phase_content,
                          module__project__is_draft=True)
    module = phase.module
    project = phase.module.project
    # TODO: what to do with the other phases that are not used?

    anonymous = AnonymousUser()
    moderator = project.moderators.first()
    initiator = project.organisation.initiators.first()

    assert project.is_draft
    with freeze_time(phase.start_date + timedelta(seconds=1)):
        assert not rules.has_perm(perm_name, anonymous, module)
        # FIXME: why are they allowed to add content to drafted projects
        # assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)


@pytest.mark.django_db
def test_rules_archived(phase_factory, user):
    assert rules.perm_exists(perm_name)

    phase_content = phases.CollectPhase()
    phase = phase_factory(phase_content=phase_content,
                          module__project__is_archived=True)
    module = phase.module
    project = phase.module.project
    # TODO: what to do with the other phases that are not used?

    anonymous = AnonymousUser()
    moderator = project.moderators.first()
    initiator = project.organisation.initiators.first()

    assert project.is_archived
    with freeze_time(phase.end_date + timedelta(seconds=1)):
        assert not rules.has_perm(perm_name, anonymous, module)
        # FIXME: why are they allowed to add content to archived projects
        assert not rules.has_perm(perm_name, user, module)
        assert rules.has_perm(perm_name, moderator, module)
        assert rules.has_perm(perm_name, initiator, module)
