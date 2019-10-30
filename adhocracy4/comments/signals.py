from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from adhocracy4 import generics

from .models import Comment

generics.setup_delete_signals(settings.A4_COMMENTABLES, Comment)


@receiver(post_save, sender=Comment)
def update_last_discussed(sender, instance, **kwargs):
    if hasattr(instance.content_object, 'last_discussed'):
        last_discussed = instance.created
        if (instance.last_discussed
                and instance.last_discussed > last_discussed):
            last_discussed = instance.last_discussed
        instance.content_object.last_discussed = last_discussed
        instance.content_object.save(
            ignore_modified=True,
            update_fields=['last_discussed']
        )
