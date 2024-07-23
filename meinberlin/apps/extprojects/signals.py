from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

from meinberlin.apps.extprojects.models import ExternalProject
from meinberlin.apps.projects.tasks import set_cache_for_projects


@receiver(post_save, sender=ExternalProject)
@receiver(post_delete, sender=ExternalProject)
def reset_cache(sender, instance, *args, **kwargs):
    """Refresh external projects cache on save or delete"""
    set_cache_for_projects.delay_on_commit(
        projects=False, get_next_projects=False, ext_projects=True, plans=False
    )
