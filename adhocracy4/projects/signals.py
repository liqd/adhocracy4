from django.db.models.signals import post_delete, post_init, post_save
from django.dispatch import receiver

from adhocracy4.images import services

from .models import Project


@receiver(post_init)
def backup_image_path(sender, instance, **kwargs):
    if issubclass(sender, Project):
        instance._current_image_file = instance.image


@receiver(post_save)
def delete_old_image(sender, instance, **kwargs):
    if issubclass(sender, Project):
        if hasattr(instance, '_current_image_file'):
            if instance._current_image_file != instance.image:
                services.delete_images([instance._current_image_file])


@receiver(post_delete)
def delete_images_for_project(sender, instance, **kwargs):
    if issubclass(sender, Project):
        services.delete_images([instance.image])
