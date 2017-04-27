from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from adhocracy4.projects.models import Project

from . import verbs


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
    verb = models.CharField(max_length=255, db_index=True, choices=verbs.all())
    description = models.TextField(blank=True, null=True)

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
