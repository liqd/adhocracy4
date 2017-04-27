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


post_save.connect(autofollow_hook, 'a4comments.Comment')
post_save.connect(autofollow_hook, 'euth_ideas.Idea')
