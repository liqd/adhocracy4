from django.core.cache import cache
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Plan


@receiver(post_save, sender=Plan)
@receiver(post_delete, sender=Plan)
def reset_cache(sender, instance, *args, **kwargs):
    cache.delete("plans")
