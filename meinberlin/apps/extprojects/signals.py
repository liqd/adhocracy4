from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ExternalProject


@receiver(post_save, sender=ExternalProject)
def reset_cache(sender, instance, update_fields, **kwargs):
    cache.delete("extprojects")
