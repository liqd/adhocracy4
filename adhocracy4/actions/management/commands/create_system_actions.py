from datetime import timedelta

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from adhocracy4.actions.models import Action
from adhocracy4.actions.verbs import Verbs
from adhocracy4.phases.models import Phase
from adhocracy4.projects.models import Project


class Command(BaseCommand):
    help = 'Create system actions.'

    def __init__(self):
        if hasattr(settings, 'A4_ACTIONS_PHASE_STARTED_HOURS'):
            self.phase_started_hours = settings.A4_ACTIONS_PHASE_STARTED_HOURS
        else:
            self.phase_started_hours = 1

        if hasattr(settings, 'A4_ACTIONS_PHASE_ENDS_HOURS'):
            self.phase_ends_hours = settings.A4_ACTIONS_PHASE_ENDS_HOURS
        else:
            self.phase_ends_hours = 24

        if hasattr(settings, 'A4_ACTIONS_PROJECT_STARTED_HOURS'):
            self.project_started_hours = \
                settings.A4_ACTIONS_PROJECTED_START_HOURS
        else:
            self.project_started_hours = 1

    def handle(self, *args, **options):
        self._phase_started()
        self._phase_ends()
        self._project_started()

    def _phase_started(self):
        phase_ct = ContentType.objects.get_for_model(Phase)

        phases = Phase.objects.start_last(hours=self.phase_started_hours)
        for phase in phases:
            project = phase.module.project
            existing_action = Action.objects.filter(
                project=project,
                verb=Verbs.START.value,
                obj_content_type=phase_ct,
                obj_object_id=phase.id
            ).first()

            if not existing_action:
                Action.objects.create(
                    project=project,
                    verb=Verbs.START.value,
                    obj=phase,
                    timestamp=phase.start_date
                )

            elif existing_action.timestamp < phase.start_date:
                # If the first phases start has been modified and moved
                # ahead, the existing actions timestamp has be adapted to
                # the actual project start.
                existing_action.timestamp = phase.start_date
                existing_action.save()

    def _phase_ends(self):
        phase_ct = ContentType.objects.get_for_model(Phase)

        phases = Phase.objects.finish_next(hours=self.phase_ends_hours)
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
                or (existing_action.timestamp +
                    timedelta(hours=self.phase_ends_hours)) < phase.end_date:

                Action.objects.create(
                    project=project,
                    verb=Verbs.SCHEDULE.value,
                    obj=phase,
                )

    def _project_started(self):
        project_ct = ContentType.objects.get_for_model(Project)

        phases = Phase.objects.start_last(hours=self.project_started_hours)
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
