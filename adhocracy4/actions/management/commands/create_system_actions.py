from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from adhocracy4.actions.models import Action
from adhocracy4.actions.verbs import Verbs
from adhocracy4.phases.models import Phase
from adhocracy4.projects.models import Project


class Command(BaseCommand):
    help = 'Create system actions.'

    def handle(self, *args, **options):
        self._phase_end_tomorrow()
        self._project_start_last_hour()

    def _phase_end_tomorrow(self):
        phase_ct = ContentType.objects.get_for_model(Phase)

        phases = Phase.objects.finish_next(hours=24)
        for phase in phases:
            project = phase.module.project
            existing_action = Action.objects.filter(
                project=project,
                verb=Verbs.SCHEDULE.value,
                obj_content_type=phase_ct,
                obj_object_id=phase.id
            ).first()

            # If the phases end has been modified and moved more than 24 hours
            # ahead, a new phase schedule action is created
            if not existing_action \
                or (existing_action.timestamp + timedelta(hours=24)) \
                    < phase.end_date:

                Action.objects.create(
                    project=project,
                    verb=Verbs.SCHEDULE.value,
                    obj=phase,
                )

    def _project_start_last_hour(self):
        project_ct = ContentType.objects.get_for_model(Project)

        phases = Phase.objects.start_last(hours=1)
        for phase in phases:
            if phase.is_first_of_project():
                project = phase.module.project
                existing_action = Action.objects.filter(
                    project=project,
                    verb=Verbs.START.value,
                    obj_content_type=project_ct,
                    obj_object_id=project.id
                ).first()

                if not existing_action:
                    Action.objects.create(
                        project=project,
                        verb=Verbs.START.value,
                        obj=project,
                        timestamp=phase.start_date
                    )

                elif existing_action.timestamp < phase.start_date:
                    # If the first phases start has been modified and moved
                    # ahead, the existing actions timestamp has be adapted to
                    # the actual project start.
                    existing_action.timestamp = phase.start_date
                    existing_action.save()
