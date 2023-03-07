from django.core.cache import cache
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from adhocracy4.dashboard import signals as a4dashboard_signals
from adhocracy4.projects.models import Project


@receiver(a4dashboard_signals.project_created)
@receiver(a4dashboard_signals.project_published)
@receiver(a4dashboard_signals.project_unpublished)
def post_dashboard_signal_delete(sender, project, user, **kwargs):
    cache.delete_many(
        [
            "projects_active*",
            "projects_future*",
            "projects_past*",
            "private_projects",
            "extprojects",
        ]
    )


@receiver(post_save, sender=Project)
@receiver(pre_delete, sender=Project)
def post_save_delete(sender, instance, update_fields=None, **kwargs):
    """
    Delete cache for project list views.
    Capture any new phases that may got created/updated while saving a project.
    """

    cache.delete_many(
        [
            "projects_active*",
            "projects_future*",
            "projects_past*",
            "private_projects",
            "extprojects",
        ]
    )
