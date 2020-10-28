from collections import OrderedDict

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from adhocracy4.projects.enums import Access
from adhocracy4.projects.models import Project

from . import verbs

_ACTION_TYPES = {}
_DEFAULT_TYPE = 'unknown'
_ACTION_ICONS = OrderedDict()
_DEFAULT_ICON = 'star'


def configure_type(type, *content_types):
    for content_type in content_types:
        _ACTION_TYPES[content_type] = type


def configure_icon(icon, *, type=None, verb=None):
    if verb is not None:
        verb = verb.value
    _ACTION_ICONS[(type, verb)] = icon


class ActionQuerySet(models.QuerySet):
    def filter_public(self):
        return self.filter(
            (
                models.Q(project__is_draft=False)
                & (models.Q(project__access=Access.PUBLIC) |
                   models.Q(project__access=Access.SEMIPUBLIC))
            )
            | models.Q(project__isnull=True)
        )

    def exclude_updates(self):
        return self.exclude(verb=verbs.Verbs.UPDATE.value)


class Action(models.Model):

    # actor, if actor is None the action was create by the system
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    # target eg. idea
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='target'
    )
    target_object_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    target = GenericForeignKey(
        ct_field='target_content_type',
        fk_field='target_object_id'
    )

    # action object eg. comment
    obj_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='obj')
    obj_object_id = models.CharField(
        max_length=255, blank=True, null=True)
    obj = GenericForeignKey(
        ct_field='obj_content_type',
        fk_field='obj_object_id')

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, blank=True, null=True)

    timestamp = models.DateTimeField(default=timezone.now)
    public = models.BooleanField(default=True, db_index=True)
    verb = models.CharField(
        max_length=255,
        db_index=True,
        choices=verbs.choices())
    description = models.TextField(blank=True, null=True)

    objects = ActionQuerySet.as_manager()

    class Meta:
        ordering = ('-timestamp',)
        index_together = [('obj_content_type', 'obj_object_id')]

    def __str__(self):

        ctx = {
            'actor': self.actor.username if self.actor else 'system',
            'verb': self.verb,
            'object': self.obj,
            'target': self.target
        }

        if self.target:
            if self.actor:
                return '{actor} {verb} {object} to {target}'.format(**ctx)
            else:
                return '{verb} {object} to {target}'.format(**ctx)
        elif self.actor:
            return '{actor} {verb} {object}'.format(**ctx)
        else:
            return '{verb} {object}'.format(**ctx)

    @property
    def type(self):
        ct = self.obj_content_type
        return _ACTION_TYPES.get((ct.app_label, ct.model), _DEFAULT_TYPE)

    @property
    def icon(self):
        for (type, verb), icon in _ACTION_ICONS.items():
            type_matches = type is None or type == self.type
            action_matches = verb is None or verb == self.verb

            if type_matches and action_matches:
                return icon
        return _DEFAULT_ICON
