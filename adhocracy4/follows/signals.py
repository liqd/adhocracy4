from django.conf import settings
from django.db.models.signals import post_save

from . import models


def autofollow_hook(instance, **kwargs):
    if hasattr(instance.project, 'id'):
        models.Follow.objects.get_or_create(
            project=instance.project,
            creator=instance.creator,
            defaults={
                'enabled': True,
            })


for model in settings.A4_AUTO_FOLLOWABLES:
    post_save.connect(autofollow_hook, model)
