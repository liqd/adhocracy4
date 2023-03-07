from django.core.cache import cache
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Plan


@receiver(post_save, sender=Plan)
@receiver(pre_delete, sender=Plan)
def reset_cache(sender, instance, update_fields=None, **kwargs):
    cache.delete("plans")
