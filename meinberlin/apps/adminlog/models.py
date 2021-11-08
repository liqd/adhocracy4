from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.translation import gettext_lazy as _

from adhocracy4.modules.models import Module
from adhocracy4.projects.models import Project

PROJECT_COMPONENT_UPDATED = 1
MODULE_COMPONENT_UPDATED = 2
PROJECT_CREATED = 3
PROJECT_PUBLISHED = 4
PROJECT_UNPUBLISHED = 5
MODULE_CREATED = 6
MODULE_PUBLISHED = 7
MODULE_UNPUBLISHED = 8

ACTION_CHOICES = (
    (PROJECT_COMPONENT_UPDATED, _('Project updated')),
    (MODULE_COMPONENT_UPDATED, _('Module updated')),
    (PROJECT_CREATED, _('Project created')),
    (PROJECT_PUBLISHED, _('Project published')),
    (PROJECT_UNPUBLISHED, _('Project unpublished')),
    (MODULE_CREATED, _('Module created')),
    (MODULE_PUBLISHED, _('Module published')),
    (MODULE_UNPUBLISHED, _('Module unpublished'))
)


class LogEntry(models.Model):
    timestamp = models.DateTimeField(default=timezone.now,
                                     editable=False,
                                     verbose_name=_('action time'))
    actor = models.ForeignKey(settings.AUTH_USER_MODEL,
                              models.SET_NULL,
                              null=True,
                              verbose_name=_('User'),
                              related_name='+')
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                verbose_name=_('Project'),
                                related_name='+')
    module = models.ForeignKey(Module,
                               on_delete=models.CASCADE,
                               null=True,
                               verbose_name=_('Module'),
                               related_name='+')
    component_identifier = models.CharField(blank=True,
                                            max_length=255)
    message = models.TextField(verbose_name=_('Message'))
    action = models.SmallIntegerField(choices=ACTION_CHOICES,
                                      verbose_name=_('Action'))

    class Meta:
        verbose_name = _('log entry')
        verbose_name_plural = _('log entries')
        ordering = ('-timestamp',)

    def __repr__(self):
        return force_text(self.timestamp)

    def __str__(self):
        return self.message
