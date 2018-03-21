from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from adhocracy4 import transforms
from adhocracy4.models import base
from adhocracy4.projects import models as project_models
from adhocracy4.files.fields import ConfiguredFileField


class OfflineEvent(base.TimeStampedModel):
    slug = AutoSlugField(populate_from='name', unique=True)
    name = models.CharField(max_length=120, verbose_name=_('Title'))
    date = models.DateTimeField(verbose_name=_('Date'))
    description = RichTextUploadingField(
        config_name='image-editor', verbose_name=_('Description'))
    project = models.ForeignKey(
        project_models.Project, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description = transforms.clean_html_field(
            self.description, 'image-editor')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('offlineevent-detail', kwargs=dict(slug=self.slug))


class OfflineEventDocument(base.TimeStampedModel):
    title = models.CharField(max_length=256)
    document = ConfiguredFileField(
        'offlineevents',
        verbose_name=_('Document'),
        help_prefix=_(
            'The document may be downloaded from the event page.'
        ),
        upload_to='offlineevents/documents',
    )
    offlineevent = models.ForeignKey(OfflineEvent,
                                     related_name='documents')
