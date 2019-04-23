from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from adhocracy4 import generics

from .models import Comment

generics.setup_delete_signals(settings.A4_COMMENTABLES, Comment)


@receiver(post_save, sender=Comment)
def update_last_discussed(sender, instance, **kwargs):
    if hasattr(instance.content_object, 'last_discussed'):
        if instance.modified:
            instance.content_object.last_discussed = instance.modified
        else:
            instance.content_object.last_discussed = instance.created
        instance.content_object.save(ignore_modified=True)
