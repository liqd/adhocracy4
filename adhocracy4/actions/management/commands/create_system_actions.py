from datetime import timedelta

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils import timezone

from adhocracy4.actions.models import Action
from adhocracy4.actions.verbs import Verbs
from adhocracy4.phases.models import Phase
from adhocracy4.projects.models import Project


class Command(BaseCommand):
    help = "Create system actions."

    def __init__(self):
        super().__init__()
        if hasattr(settings, "A4_ACTIONS_PHASE_STARTED_HOURS"):
            self.phase_started_hours = settings.A4_ACTIONS_PHASE_STARTED_HOURS
        else:
            self.phase_started_hours = 1

        if hasattr(settings, "A4_ACTIONS_PHASE_ENDS_HOURS"):
            self.phase_ends_hours = settings.A4_ACTIONS_PHASE_ENDS_HOURS
        else:
            self.phase_ends_hours = 24

        if hasattr(settings, "A4_ACTIONS_PROJECT_STARTED_HOURS"):
            self.project_started_hours = settings.A4_ACTIONS_PROJECTED_START_HOURS
        else:
            self.project_started_hours = 1

    def handle(self, *args, **options):
        self._phase_started()
        self._phase_ends()
        self._project_started()

    def _phase_started(self):
        """Create an action for every phase that started.

        The timespan in which the phases were started can be set
        in the project with A4_ACTIONS_PHASE_STARTED_HOURS.
        In the projects this is used to notify users if a phase has started.
        """
        phase_ct = ContentType.objects.get_for_model(Phase)

        phases = (
            Phase.objects.filter(module__is_draft=False)
            .filter(module__project__is_draft=False)
            .start_last(hours=self.phase_started_hours)
        )
        for phase in phases:
            project = phase.module.project
            existing_action = Action.objects.filter(
                project=project,
                verb=Verbs.START.value,
                obj_content_type=phase_ct,
                obj_object_id=phase.id,
            ).first()

            if not existing_action:
                Action.objects.create(
                    project=project,
                    verb=Verbs.START.value,
                    obj=phase,
                    timestamp=phase.start_date,
                )

            elif existing_action.timestamp < phase.start_date:
                # If the first phases start has been modified and moved
                # ahead, the existing actions timestamp has be adapted to
                # the actual project start.
                existing_action.timestamp = phase.start_date
                existing_action.save()

    def _phase_ends(self):
        """Create an action for every phase that ends soon OR is a one-day event starting soon."""
        phase_ct = ContentType.objects.get_for_model(Phase)
        now = timezone.now()

        # Get the configured hours (default 72 for offline events, 24 for regular phases)
        offline_hours = getattr(settings, "ACTIONS_OFFLINE_EVENT_STARTING_HOURS", 72)
        phase_hours = self.phase_ends_hours  # Regular 24h setting

        # 1. Regular phases ending soon (original logic)
        ending_soon = Phase.objects.filter(
            module__is_draft=False, module__project__is_draft=False
        ).finish_next(hours=phase_hours)

        # 2. One-day phases (offline events) starting within offline_hours
        starting_soon = Phase.objects.filter(
            module__is_draft=False,
            module__project__is_draft=False,
            type__contains="offline-event",  # Todo: confirm since this type is mB only, okay to leave here for a+ forks
            start_date__gte=now,
            start_date__lte=now + timedelta(hours=offline_hours),
        )

        # Process regular ending phases (keep original SCHEDULE logic)
        for phase in ending_soon:
            project = phase.module.project
            existing_action = Action.objects.filter(
                project=project,
                verb=Verbs.SCHEDULE.value,
                obj_content_type=phase_ct,
                obj_object_id=phase.id,
            ).first()

            # If the phases end has been modified and moved more than 24 hours
            # ahead, a new phase schedule action is created
            if (
                not existing_action
                or (existing_action.timestamp + timedelta(hours=self.phase_ends_hours))
                < phase.end_date
            ):
                Action.objects.create(
                    project=project,
                    verb=Verbs.SCHEDULE.value,
                    obj=phase,
                )

        # Process offline event phases with 72-hour logic
        for phase in starting_soon:
            project = phase.module.project
            existing_action = Action.objects.filter(
                project=project,
                verb=Verbs.SCHEDULE.value,
                obj_content_type=phase_ct,
                obj_object_id=phase.id,
            ).first()

            # Create if no action exists, or if the last action is too old
            if not existing_action:
                Action.objects.create(
                    project=project,
                    verb=Verbs.SCHEDULE.value,
                    obj=phase,
                    timestamp=phase.start_date,  # Use the event date as timestamp
                )
            elif (
                existing_action.timestamp + timedelta(hours=offline_hours)
            ) < phase.start_date:
                # Event date was moved forward - create new action
                Action.objects.create(
                    project=project,
                    verb=Verbs.SCHEDULE.value,
                    obj=phase,
                    timestamp=phase.start_date,
                )
            elif existing_action.timestamp != phase.start_date:
                # Event date changed but still within window - update timestamp
                existing_action.timestamp = phase.start_date
                existing_action.save()

    def _project_started(self):
        """Create an action when a project has started.

        The timespan in which the project has started can be set
        in the project with A4_ACTIONS_PROJECT_STARTED_HOURS.
        We do not use this action for notifications, but display
        it in some lists of actions.
        """
        project_ct = ContentType.objects.get_for_model(Project)

        phases = Phase.objects.start_last(hours=self.project_started_hours).exclude(
            module__project__is_draft=True
        )
        for phase in phases:
            if phase.starts_first_of_project():
                project = phase.module.project
                existing_action = Action.objects.filter(
                    project=project,
                    verb=Verbs.START.value,
                    obj_content_type=project_ct,
                    obj_object_id=project.id,
                ).first()

                if not existing_action:
                    Action.objects.create(
                        project=project,
                        verb=Verbs.START.value,
                        obj=project,
                        timestamp=phase.start_date,
                    )

                elif existing_action.timestamp < phase.start_date:
                    # If the first phase start has been modified and moved
                    # ahead, the existing actions timestamp has to be adapted
                    # to the actual project start.
                    existing_action.timestamp = phase.start_date
                    existing_action.save()
