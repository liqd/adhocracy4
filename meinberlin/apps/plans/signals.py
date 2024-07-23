from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

from meinberlin.apps.plans.models import Plan
from meinberlin.apps.projects.tasks import set_cache_for_projects


@receiver(post_save, sender=Plan)
@receiver(post_delete, sender=Plan)
def reset_cache(sender, instance, *args, **kwargs):
    """Refresh plan cache on save or delete"""
    set_cache_for_projects.delay_on_commit(
        projects=False, get_next_projects=False, ext_projects=False, plans=True
    )
