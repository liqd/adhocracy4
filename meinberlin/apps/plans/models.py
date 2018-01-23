from ckeditor.fields import RichTextField
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from adhocracy4 import transforms
from adhocracy4.maps import fields as map_fields
from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.projects import models as project_models
from meinberlin.apps.maps.models import MapPreset

STATUS_TODO = 0
STATUS_PLANNING = 1
STATUS_IMPLEMENTATION = 2
STATUS_DONE = 3
STATUS_STOPPED = 4

PARTICIPATION_NO = 0
PARTICIPATION_YES = 1
PARTICIPATION_UNDECIDED = 2


class Plan(UserGeneratedContentModel):
    title = models.CharField(max_length=120, verbose_name=_('Title'))
    organisation = models.ForeignKey(
        settings.A4_ORGANISATIONS_MODEL,
        on_delete=models.CASCADE)
    project = models.ForeignKey(project_models.Project, blank=True, null=True)
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
        limit_choices_to=Q(category__name='Berlin') & ~Q(name='Berlin'))
    contact = models.TextField(max_length=255, verbose_name=_('Contact'))
    cost = models.PositiveIntegerField(blank=True, null=True,
                                       verbose_name=_('Cost'))
    description = RichTextField(verbose_name=_('Description'), blank=True)
    category = models.CharField(max_length=255, verbose_name=_('Type of plan'))
    status = models.SmallIntegerField(choices=(
        (STATUS_TODO, _('Idea')),
        (STATUS_PLANNING, _('Planning')),
        (STATUS_IMPLEMENTATION, _('Implementation')),
        (STATUS_DONE, _('Done')),
        (STATUS_STOPPED, _('Stopped')),
    ))
    participation = models.SmallIntegerField(choices=(
        (PARTICIPATION_YES, _('Yes')),
        (PARTICIPATION_NO, _('No')),
        (PARTICIPATION_UNDECIDED, _('Still undecided')),
    ))

    class Meta:
        ordering = ['-created']

    @property
    def reference_number(self):
        return '{:d}-{:05d}'.format(self.created.year, self.pk)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('meinberlin_plans:plan-detail',
                       kwargs=dict(pk=self.pk, year=self.created.year))

    def save(self, *args, **kwargs):
        self.description = transforms.clean_html_field(self.description)
        super().save(*args, **kwargs)
