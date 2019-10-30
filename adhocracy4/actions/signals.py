from itertools import chain

from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete
from django.db.models.signals import post_save

from .models import Action
from .verbs import Verbs

# Actions resulting from the create_system_actions management call
SYSTEM_ACTIONABLES = (
    ('a4phases', 'Phase'),
    ('a4projects', 'Project')
)


def _extract_target(instance):
    target = None
    if hasattr(instance, 'content_object'):
        target = instance.content_object
    elif hasattr(instance, 'project'):
        target = instance.project
    return target


def _add_action(sender, instance, created, update_fields, **kwargs):
    if not update_fields or 'last_discussed' not in update_fields:
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

        if hasattr(instance, 'project'):
            action.project = instance.project

        action.save()


for app, model in settings.A4_ACTIONABLES:
    post_save.connect(_add_action, apps.get_model(app, model))


def _delete_action(sender, instance, **kwargs):
    contenttype = ContentType.objects.get_for_model(sender)
    Action.objects\
        .filter(obj_content_type=contenttype, obj_object_id=instance.id)\
        .delete()


for app, model in chain(SYSTEM_ACTIONABLES, settings.A4_ACTIONABLES):
    post_delete.connect(_delete_action, apps.get_model(app, model))
