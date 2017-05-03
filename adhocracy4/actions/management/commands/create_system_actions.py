from django.core.management.base import BaseCommand

from adhocracy4.phases.models import Phase
from adhocracy4.actions.models import Action
from adhocracy4.actions.verbs import Verbs


class Command(BaseCommand):
    help = 'Create system actions.'

    def handle(self, *args, **options):
        self._phase_end_tomorrow()

    def _phase_end_tomorrow(self):
        phases = Phase.objects.finish_next()

        for phase in phases:
            project = phase.module.project
            existing_action = Action.objects.filter(
                project=project,
                verb=Verbs.COMPLETE.value,
                timestamp=phase.end_date,
            )

            if not existing_action:
                Action.objects.create(
                    project=project,
                    verb=Verbs.COMPLETE.value,
                    timestamp=phase.end_date,
                    obj=phase,
                )
