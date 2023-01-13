from datetime import timedelta

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from adhocracy4.actions.models import Action
from adhocracy4.actions.verbs import Verbs
from meinberlin.apps.offlineevents.models import OfflineEvent


class Command(BaseCommand):
    help = "Create offlineevent system actions."

    def __init__(self):
        if hasattr(settings, "ACTIONS_OFFLINE_EVENT_STARTING_HOURS"):
            self.event_starting_hours = settings.ACTIONS_OFFLINE_EVENT_STARTING_HOURS
        else:
            self.event_starting_hours = 72

    def handle(self, *args, **options):
        self._event_starting()

    def _event_starting(self):
        event_ct = ContentType.objects.get_for_model(OfflineEvent)

        events = OfflineEvent.objects.starts_within(hours=self.event_starting_hours)
        for event in events:
            existing_action = Action.objects.filter(
                project=event.project,
                verb=Verbs.START.value,
                obj_content_type=event_ct,
                obj_object_id=event.id,
            ).first()

            # If the event date has been modified and moved more than
            # event_starting_hours ahead, schedule a new action
            if (
                not existing_action
                or (
                    existing_action.timestamp
                    + timedelta(hours=self.event_starting_hours)
                )
                < event.date
            ):
                Action.objects.create(
                    project=event.project,
                    verb=Verbs.START.value,
                    obj=event,
                    timestamp=event.date,
                )
            elif existing_action.timestamp != event.date:
                existing_action.timestamp = event.date
                existing_action.save()
