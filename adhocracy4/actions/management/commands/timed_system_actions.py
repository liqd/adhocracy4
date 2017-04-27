from django.core.management.base import BaseCommand

from adhocracy4.phases.models import Phase
from adhocracy4.actions import verbs
from adhocracy4.actions.models import Action


class Command(BaseCommand):
    help = 'Create actions that depend time.'

    def handle(self, *args, **options):
        self._phase_end_tomorrow()

    def _phase_end_tomorrow(self):
        phases = Phase.objects.finish_next()

        for phase in phases:
            project = phase.module.project
            existing_action = Action.objects.filter(
                project=project,
                verb=verbs.COMPLETE,
                timestamp=phase.end_date,
            )

            if not existing_action:
                Action.objects.create(
                    project=project,
                    verb=verbs.COMPLETE,
                    timestamp=phase.end_date,
                    obj=phase,
                )
