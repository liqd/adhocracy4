from datetime import timedelta

import pytest
import rules
from django.contrib.auth.models import AnonymousUser
from freezegun import freeze_time

from apps.ideas import phases

perm_name = 'meinberlin_ideas.rate_idea'


@pytest.mark.django_db
def test_rules_pre_phase(phase_factory, idea_factory, user):
    assert rules.perm_exists(perm_name)

    phase_content = phases.CollectPhase()
    phase = phase_factory(phase_content=phase_content)
    module = phase.module
    project = phase.module.project
    item = idea_factory(module=module)
    # TODO: what to do with the other phases that are not used?

    anonymous = AnonymousUser()
    moderator = project.moderators.first()
    initiator = project.organisation.initiators.first()

    assert project.is_public
    with freeze_time(phase.start_date - timedelta(days=1)):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)


@pytest.mark.django_db
def test_rules_public(phase_factory, idea_factory, user):
    assert rules.perm_exists(perm_name)

    phase_content = phases.CollectPhase()
    phase = phase_factory(phase_content=phase_content)
    module = phase.module
    project = phase.module.project
    item = idea_factory(module=module)
    # TODO: what to do with the other phases that are not used?

    anonymous = AnonymousUser()
    moderator = project.moderators.first()
    initiator = project.organisation.initiators.first()

    assert project.is_public
    with freeze_time(phase.start_date + timedelta(seconds=1)):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)


@pytest.mark.django_db
def test_rules_draft(phase_factory, idea_factory, user):
    assert rules.perm_exists(perm_name)

    phase_content = phases.CollectPhase()
    phase = phase_factory(phase_content=phase_content,
                          module__project__is_draft=True)
    module = phase.module
    project = phase.module.project
    item = idea_factory(module=module)
    # TODO: what to do with the other phases that are not used?

    anonymous = AnonymousUser()
    moderator = project.moderators.first()
    initiator = project.organisation.initiators.first()

    assert project.is_draft
    with freeze_time(phase.start_date + timedelta(seconds=1)):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)


@pytest.mark.django_db
def test_rules_archived(phase_factory, idea_factory, user):
    assert rules.perm_exists(perm_name)

    phase_content = phases.CollectPhase()
    phase = phase_factory(phase_content=phase_content,
                          module__project__is_archived=True)
    module = phase.module
    project = phase.module.project
    item = idea_factory(module=module)
    # TODO: what to do with the other phases that are not used?

    anonymous = AnonymousUser()
    moderator = project.moderators.first()
    initiator = project.organisation.initiators.first()

    assert project.is_archived
    with freeze_time(phase.end_date + timedelta(seconds=1)):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)
