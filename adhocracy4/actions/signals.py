from django.apps import apps
from django.conf import settings
from django.db.models.signals import post_save

from .models import Action
from .verbs import Verbs


def _extract_target(instance):
    target = None
    if hasattr(instance, 'content_object'):
        target = instance.content_object
    elif hasattr(instance, 'project'):
        target = instance.project
    return target


def add_action(sender, instance, created, **kwargs):
    actor = instance.creator if hasattr(instance, 'creator') else None
    target = None
    if created:
        target = _extract_target(instance)
        if target:
            verb = Verbs.ADD.value
        else:
            verb = Verbs.CREATE.value

    else:
        verb = Verbs.UPDATE.value

    action = Action(
        actor=actor,
        verb=verb,
        obj=instance,
        target=target,
    )

    # TODO: this could be extended
    if hasattr(instance, 'project'):
        action.project = instance.project

    action.save()


for app, model in settings.A4_ACTIONABLES:
    post_save.connect(add_action, apps.get_model(app, model))
