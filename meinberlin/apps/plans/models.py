from ckeditor.fields import RichTextField
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from adhocracy4 import transforms
from adhocracy4.images.fields import ConfiguredImageField
from adhocracy4.maps import fields as map_fields
from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.projects import models as project_models
from meinberlin.apps.maps.models import MapPreset


class Plan(UserGeneratedContentModel):

    PARTICIPATION_NO = 0
    PARTICIPATION_YES = 1
    PARTICIPATION_UNDECIDED = 2
    PARTICIPATION_CHOICES = (
        (PARTICIPATION_YES, _('Yes')),
        (PARTICIPATION_NO, _('No')),
        (PARTICIPATION_UNDECIDED, _('Still undecided')),
    )

    STATUS_TODO = 0
    STATUS_PLANNING = 1
    STATUS_IMPLEMENTATION = 2
    STATUS_DONE = 3
    STATUS_STOPPED = 4
    STATUS_CHOICES = (
        (STATUS_TODO, _('Idea')),
        (STATUS_PLANNING, _('Planning')),
        (STATUS_IMPLEMENTATION, _('Implementation')),
        (STATUS_DONE, _('Done')),
        (STATUS_STOPPED, _('Stopped')),
    )

    title = models.CharField(max_length=120, verbose_name=_('Title'))
    organisation = models.ForeignKey(
        settings.A4_ORGANISATIONS_MODEL,
        on_delete=models.CASCADE)
    projects = models.ManyToManyField(
        project_models.Project,
        related_name='plans',
        blank=True
    )
    point = map_fields.PointField(
        verbose_name=_('Where can the plan be located on a map?'),
        help_text=_('Click inside marked area on the map to set a marker. '
                    'Drag and drop the marker to change its place. '
                    'Alternatively you can use the search field to search '
                    'for an address.'))
    point_label = models.CharField(
        blank=True,
        default='',
        max_length=255,
        verbose_name=_('Label of the location'),
        help_text=_('This could be an address or the name of a landmark.'),
    )
    district = models.ForeignKey(
        MapPreset,
        limit_choices_to=Q(category__name='Bezirke - Berlin'),
        verbose_name=_('District')
    )
    contact = models.TextField(max_length=255, verbose_name=_('Contact'))
    cost = models.PositiveIntegerField(blank=True, null=True,
                                       verbose_name=_('Cost'))
    description = RichTextField(verbose_name=_('Description'))
    description_image = ConfiguredImageField(
        'description_image',
        verbose_name=_('Description Image'),
        help_prefix=_(
            'This image will be shown together with the description'
        ),
        upload_to='plan/description_image',
        blank=True)
    category = models.CharField(max_length=255, verbose_name=_('Type of plan'))
    status = models.SmallIntegerField(choices=STATUS_CHOICES)
    participation = models.SmallIntegerField(
        choices=PARTICIPATION_CHOICES,
        verbose_name=_('Participation')
    )

    class Meta:
        ordering = ['-created']

    @property
    def reference_number(self):
        return '{:d}-{:05d}'.format(self.created.year, self.pk)

    @cached_property
    def published_projects(self):
        return self.projects.filter(
            is_draft=False, is_public=True, is_archived=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('meinberlin_plans:plan-detail',
                       kwargs=dict(pk='{:05d}'.format(self.pk),
                                   year=self.created.year))

    def save(self, *args, **kwargs):
        self.description = transforms.clean_html_field(self.description)
        super().save(*args, **kwargs)
