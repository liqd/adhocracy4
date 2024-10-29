from django.apps import apps
from django.conf import settings
from django.db.models.signals import post_save

from . import models


def autofollow_hook(instance, **kwargs):
    """Hook which makes a user automatically follow a project they created content
    in. Used in cominbation with the post_save signal for all models defined in
    settings.A4_AUTO_FOLLOWABLES. Content by unregistered users needs to be ignored,
    hence the check for instance.creator"""
    if hasattr(instance.project, "id") and instance.creator:
        models.Follow.objects.get_or_create(
            project=instance.project,
            creator=instance.creator,
            defaults={
                "enabled": True,
            },
        )


for app, model in settings.A4_AUTO_FOLLOWABLES:
    post_save.connect(autofollow_hook, apps.get_model(app, model))
