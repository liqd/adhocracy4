from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

from adhocracy4.dashboard import signals as a4dashboard_signals
from adhocracy4.phases.models import Phase
from adhocracy4.projects.models import Project
from meinberlin.apps.projects.tasks import set_cache_for_projects


@receiver(a4dashboard_signals.project_created)
@receiver(a4dashboard_signals.project_published)
@receiver(a4dashboard_signals.project_unpublished)
def post_dashboard_signal_delete(sender, project, user, **kwargs):
    """Refresh project, plan and extproject cache on dashboard signal"""
    set_cache_for_projects.delay_on_commit(get_next_projects=True)


@receiver(post_save, sender=Phase)
@receiver(post_delete, sender=Phase)
def post_phase_save_delete(sender, instance, **kwargs):
    """Refresh project, plan and extproject cache on phase save or delete"""
    set_cache_for_projects.delay_on_commit(get_next_projects=True)


@receiver(post_save, sender=Project)
@receiver(post_delete, sender=Project)
def post_save_delete(sender, instance, *args, **kwargs):
    """
    Refresh cache for project list views.
    Capture any new phases that may got created/updated while saving a project.
    """
    set_cache_for_projects.delay_on_commit(
        projects=True, get_next_projects=True, ext_projects=False, plans=False
    )
