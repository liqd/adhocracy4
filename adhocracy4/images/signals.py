from django.apps import apps
from django.db.models.signals import post_delete
from django.db.models.signals import post_init
from django.db.models.signals import post_save

from adhocracy4.images import services

from .fields import ConfiguredImageField

_PREFIX = '_a4images_'
_IMAGE_FIELDS_ATTR = _PREFIX + 'image_fields'
_CURRENT_IMAGES_ATTR = _PREFIX + 'current_images'


def backup_images_path_on_init(sender, instance, **kwargs):
    backup_images_path(instance)


def backup_images_path(instance):
    image_fields = getattr(instance, _IMAGE_FIELDS_ATTR, [])
    current_images = [getattr(instance, fieldname)
                      for fieldname in image_fields]
    setattr(instance, _CURRENT_IMAGES_ATTR, current_images)


def delete_old_images_on_save(sender, instance, **kwargs):
    image_fields = getattr(instance, _IMAGE_FIELDS_ATTR, [])
    current_images = getattr(instance, _CURRENT_IMAGES_ATTR, ())

    delete_images = [current_image
                     for fieldname, current_image
                     in zip(image_fields, current_images)
                     if getattr(instance, fieldname, None) != current_image]
    services.delete_images(delete_images)

    backup_images_path(instance)


def delete_images_cascaded(sender, instance, **kwargs):
    image_fields = getattr(instance, _IMAGE_FIELDS_ATTR, [])
    images = [getattr(instance, fieldname) for fieldname in image_fields]
    services.delete_images(images)


# Setup signals for all ConfiguredImageFields
for model in apps.get_models():
    for field in model._meta.get_fields(include_parents=False):
        if isinstance(field, ConfiguredImageField):
            image_fields = getattr(model, _IMAGE_FIELDS_ATTR, [])
            if field.attname not in image_fields:
                image_fields.append(field.attname)
                setattr(model, _IMAGE_FIELDS_ATTR, image_fields)

    if hasattr(model, _IMAGE_FIELDS_ATTR):
        post_init.connect(backup_images_path_on_init, sender=model)
        post_save.connect(delete_old_images_on_save, sender=model)
        post_delete.connect(delete_images_cascaded, sender=model)
