from django.core.cache import cache
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

from adhocracy4.dashboard import signals as a4dashboard_signals
from adhocracy4.projects.models import Project
from meinberlin.apps.projects.tasks import get_next_projects_end
from meinberlin.apps.projects.tasks import get_next_projects_start


@receiver(a4dashboard_signals.project_created)
@receiver(a4dashboard_signals.project_published)
@receiver(a4dashboard_signals.project_unpublished)
def post_dashboard_signal_delete(sender, project, user, **kwargs):
    cache.delete_many(
        [
            "projects_activeParticipation",
            "projects_futureParticipation",
            "projects_pastParticipation",
            "private_projects",
            "extprojects",
        ]
    )


@receiver(post_save, sender=Project)
@receiver(post_delete, sender=Project)
def post_save_delete(sender, instance, *args, **kwargs):
    """
    Delete cache for project list views.
    Capture any new phases that may got created/updated while saving a project.
    """

    cache.delete_many(
        [
            "projects_activeParticipation",
            "projects_futureParticipation",
            "projects_pastParticipation",
            "private_projects",
            "extprojects",
        ]
    )

    # set cache for the next projects that will be published in the next 10min
    get_next_projects_start()

    # set cache for the next project that ends and should be unpublished
    get_next_projects_end()
