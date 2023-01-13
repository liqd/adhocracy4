from datetime import timedelta

import pytest
from dateutil.parser import parse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from freezegun import freeze_time

from adhocracy4.actions.models import Action
from adhocracy4.actions.verbs import Verbs
from meinberlin.apps.offlineevents.models import OfflineEvent

START = Verbs.START.value

EVENT_STARTING_HOURS = 0
if hasattr(settings, "ACTIONS_OFFLINE_EVENT_STARTING_HOURS"):
    EVENT_STARTING_HOURS = settings.ACTIONS_OFFLINE_EVENT_STARTING_HOURS
else:
    EVENT_STARTING_HOURS = 72


@pytest.mark.django_db
def test_event_date_later(offline_event_factory):

    EVENT_DATE = parse("2020-01-05 17:00:00 UTC")
    ACTION_DATE = EVENT_DATE - timedelta(hours=EVENT_STARTING_HOURS)
    CURRENT_DATE = ACTION_DATE - timedelta(minutes=30)

    content_type = ContentType.objects.get_for_model(OfflineEvent)
    offline_event_factory(
        date=EVENT_DATE,
    )

    with freeze_time(CURRENT_DATE):
        call_command("create_offlineevent_system_actions")
        action_count = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).count()
        assert action_count == 0


@pytest.mark.django_db
def test_event_date_soon(offline_event_factory):

    EVENT_DATE = parse("2020-01-05 17:00:00 UTC")
    ACTION_DATE = EVENT_DATE - timedelta(hours=EVENT_STARTING_HOURS)
    CURRENT_DATE = ACTION_DATE + timedelta(minutes=30)

    content_type = ContentType.objects.get_for_model(OfflineEvent)
    event = offline_event_factory(
        date=EVENT_DATE,
    )
    project = event.project

    action_count = Action.objects.filter(
        verb=START, obj_content_type=content_type
    ).count()
    assert action_count == 0

    with freeze_time(CURRENT_DATE):
        call_command("create_offlineevent_system_actions")
        action_count = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).count()
        action = Action.objects.filter(verb=START, obj_content_type=content_type).last()
        assert action_count == 1
        assert action.obj == event
        assert action.verb == START
        assert action.project == project


@pytest.mark.django_db
def test_phase_reschedule(offline_event_factory):

    EVENT_DATE = parse("2020-01-05 17:00:00 UTC")
    ACTION_DATE = EVENT_DATE - timedelta(hours=EVENT_STARTING_HOURS)

    content_type = ContentType.objects.get_for_model(OfflineEvent)
    event = offline_event_factory(
        date=EVENT_DATE,
    )

    # event happens soon
    CURRENT_DATE = ACTION_DATE + timedelta(minutes=30)
    with freeze_time(CURRENT_DATE):
        call_command("create_offlineevent_system_actions")
        action_count = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).count()
        assert action_count == 1

    # reschedule event date, but little enough so no new action will be created
    EVENT_DATE += timedelta(hours=EVENT_STARTING_HOURS) - timedelta(hours=1)
    ACTION_DATE = EVENT_DATE - timedelta(hours=EVENT_STARTING_HOURS)
    CURRENT_DATE = ACTION_DATE + timedelta(minutes=30)
    event.date = EVENT_DATE
    event.save()

    with freeze_time(CURRENT_DATE):
        call_command("create_offlineevent_system_actions")
        action_count = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).count()
        assert action_count == 1

    # reschedule event date again, benough so a new action will be created
    EVENT_DATE += timedelta(hours=EVENT_STARTING_HOURS) + timedelta(hours=1)
    ACTION_DATE = EVENT_DATE - timedelta(hours=EVENT_STARTING_HOURS)
    CURRENT_DATE = ACTION_DATE + timedelta(minutes=30)
    event.date = EVENT_DATE
    event.save()

    with freeze_time(CURRENT_DATE):
        call_command("create_offlineevent_system_actions")
        action_count = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).count()
        assert action_count == 2
