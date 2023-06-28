from datetime import timedelta

import pytest
from dateutil.parser import parse
from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.core.management import call_command
from freezegun import freeze_time

from adhocracy4.actions.models import Action
from adhocracy4.actions.verbs import Verbs
from adhocracy4.phases.models import Phase
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting import phases
from meinberlin.apps.offlineevents.models import OfflineEvent
from meinberlin.config import settings

START = Verbs.START.value

EVENT_STARTING_HOURS = 0
if hasattr(settings, "ACTIONS_OFFLINE_EVENT_STARTING_HOURS"):
    EVENT_STARTING_HOURS = settings.ACTIONS_OFFLINE_EVENT_STARTING_HOURS
else:
    EVENT_STARTING_HOURS = 72


@pytest.mark.django_db
def test_event_soon_email(offline_event_factory):
    EVENT_DATE = parse("2020-01-05 17:00:00 UTC")
    ACTION_DATE = EVENT_DATE - timedelta(hours=EVENT_STARTING_HOURS)
    CURRENT_DATE = ACTION_DATE + timedelta(minutes=30)

    content_type = ContentType.objects.get_for_model(OfflineEvent)
    offline_event_factory(
        date=EVENT_DATE,
    )

    action_count = Action.objects.filter(
        verb=START, obj_content_type=content_type
    ).count()
    assert action_count == 0

    with freeze_time(CURRENT_DATE):
        call_command("create_offlineevent_system_actions")
        # NotifyFollowersOnUpcomingEventEmail
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject.startswith("Einladung zu einer Veranstaltung")


@pytest.mark.django_db
def test_event_soon_draft_no_email(offline_event_factory):
    EVENT_DATE = parse("2020-01-05 17:00:00 UTC")
    ACTION_DATE = EVENT_DATE - timedelta(hours=EVENT_STARTING_HOURS)
    CURRENT_DATE = ACTION_DATE + timedelta(minutes=30)

    content_type = ContentType.objects.get_for_model(OfflineEvent)
    event = offline_event_factory(
        date=EVENT_DATE,
    )
    project = event.project
    project.is_draft = True
    project.save()
    project.refresh_from_db()

    action_count = Action.objects.filter(
        verb=START, obj_content_type=content_type
    ).count()
    assert action_count == 0

    with freeze_time(CURRENT_DATE):
        call_command("create_offlineevent_system_actions")
        action_count = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).count()
        assert action_count == 0
        # NotifyFollowersOnUpcomingEventEmail
        assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_phase_started_email(apiclient, phase_factory, proposal_factory):
    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    phase.end_date += timedelta(hours=48)
    phase.save()
    phase.refresh_from_db()

    content_type = ContentType.objects.get_for_model(Phase)
    action_count = Action.objects.filter(
        verb=START, obj_content_type=content_type
    ).count()
    assert action_count == 0

    with freeze_phase(phase):
        call_command("create_system_actions")
        action_count = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).count()
        assert action_count == 1
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject.startswith("Los geht's:")


@pytest.mark.django_db
def test_phase_started_draft_no_email(apiclient, phase_factory, proposal_factory):
    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    project = phase.module.project
    project.is_draft = True
    project.save()
    project.refresh_from_db()

    phase.end_date += timedelta(hours=48)
    phase.save()
    phase.refresh_from_db()

    content_type = ContentType.objects.get_for_model(Phase)
    action_count = Action.objects.filter(
        verb=START, obj_content_type=content_type
    ).count()
    assert action_count == 0

    with freeze_phase(phase):
        call_command("create_system_actions")
        action_count = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).count()
        assert action_count == 0
        assert len(mail.outbox) == 0
