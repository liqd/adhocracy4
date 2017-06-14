from django.apps import apps
from django.db.models.signals import post_delete, post_init, post_save

from adhocracy4.images import services
from .fields import ConfiguredImageField


def backup_images_path(sender, instance, **kwargs):
    image_fields = getattr(instance, '_image_fields', ())
    current_images = [getattr(instance, fieldname)
                      for fieldname in image_fields]
    instance._current_images = current_images


def delete_old_images(sender, instance, **kwargs):
    image_fields = getattr(instance, '_image_fields', ())
    current_images = getattr(instance, '_current_images', ())
    delattr(instance, '_current_images')

    delete_images = [current_image
                     for fieldname, current_image
                     in zip(image_fields, current_images)
                     if getattr(instance, fieldname, None) != current_image]

    services.delete_images(delete_images)


def delete_images_cascaded(sender, instance, **kwargs):
    image_fields = getattr(instance, '_image_fields', ())
    images = [getattr(instance, fieldname) for fieldname in image_fields]
    services.delete_images(images)


# Setup signals for all ConfiguredImageFields
for model in apps.get_models():
    for field in model._meta.get_fields():
        if isinstance(field, ConfiguredImageField):
            image_fields = getattr(model, '_image_fields', ())
            model._image_fields = image_fields + (field.attname, )

    if hasattr(model, '_image_fields'):
        post_init.connect(backup_images_path, sender=model)
        post_save.connect(delete_old_images, sender=model)
        post_delete.connect(delete_images_cascaded, sender=model)
