from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.projects.models import Project

PLATFORM = 0
ORGANISATION = 1
PROJECT = 2

RECEIVER_CHOICES = (
    (PROJECT, _('Users following the chosen project')),
    (ORGANISATION, _('Users following the chosen organisation')),
    (PLATFORM, _('Every user on the platform')),
)


class Newsletter(UserGeneratedContentModel):

    sender_name = models.CharField(max_length=254,
                                   verbose_name=_('Name'))
    sender = models.EmailField(blank=True,
                               verbose_name=_('Sender'))
    subject = models.CharField(max_length=254,
                               verbose_name=_('Subject'))
    body = RichTextUploadingField(blank=True,
                                  config_name='image-editor',
                                  verbose_name=_('Email body'))
    sent = models.DateTimeField(blank=True,
                                null=True,
                                verbose_name=_('Sent'))

    receivers = models.PositiveSmallIntegerField(choices=RECEIVER_CHOICES,
                                                 verbose_name=_('Receivers'),
                                                 default='')

    project = models.ForeignKey(Project,
                                null=True, blank=True,
                                on_delete=models.CASCADE)

    organisation = models.ForeignKey(settings.A4_ORGANISATIONS_MODEL,
                                     null=True, blank=True,
                                     on_delete=models.CASCADE)
