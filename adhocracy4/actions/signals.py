from django.apps import apps
from django.conf import settings
from django.db.models.signals import post_save

from adhocracy4.projects.models import Project

from . import verbs
from .models import Action


def _has_project(instance):
    return hasattr(instance, 'project') \
           and instance.project.__class__ is Project


def _extract_target(instance):
    target = None
    if hasattr(instance, 'content_object'):
        target = instance.content_object
    elif _has_project(instance):
        target = instance.project
    return target


def add_action(sender, instance, created, **kwargs):
    actor = instance.creator if hasattr(instance,'creator') else None
    target = None
    if created:
        target = _extract_target(instance)
        if target:
            verb = verbs.ADD
        else:
            verb = verbs.CREATE

    else:
        verb = verbs.UPDATE

    action = Action(
        actor=actor,
        verb=verb,
        obj=instance,
        target=target,
    )

    if _has_project(instance):
        action.project = instance.project

    action.save()


if hasattr(settings,'A4_ACTIONABLES'):
    for app, model in settings.A4_ACTIONABLES:
        post_save.connect(add_action, apps.get_model(app, model))
