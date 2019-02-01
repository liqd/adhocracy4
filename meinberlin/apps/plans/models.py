from ckeditor.fields import RichTextField
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from adhocracy4 import transforms
from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.images.fields import ConfiguredImageField
from adhocracy4.maps import fields as map_fields
from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.phases.models import Phase
from adhocracy4.projects import models as project_models
from adhocracy4.projects.fields import TopicField


class Plan(UserGeneratedContentModel):

    PARTICIPATION_YES = 0
    PARTICIPATION_NO = 1
    PARTICIPATION_UNDECIDED = 2
    PARTICIPATION_CHOICES = (
        (PARTICIPATION_YES, _('Yes')),
        (PARTICIPATION_NO, _('No')),
        (PARTICIPATION_UNDECIDED, _('Still undecided')),
    )

    STATUS_ONGOING = 0
    STATUS_DONE = 1

    STATUS_CHOICES = (
        (STATUS_ONGOING, _('Ongoing')),
        (STATUS_DONE, _('Done'))
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
        default='',
        max_length=255,
        verbose_name=_('Label of the location'),
        help_text=_('The label of the location is '
                    'displayed in the detail view of the plan'),
    )
    district = models.ForeignKey(
        AdministrativeDistrict,
        verbose_name=_('District'),
        null=True,
        blank=True
    )
    contact = models.TextField(max_length=1000, verbose_name=_('Contact'))
    cost = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name=_('Cost'))
    description = RichTextField(verbose_name=_('Description'))
    description_image = ConfiguredImageField(
        'plan_image',
        verbose_name=_('Add image'),
        upload_to='plan/description_image',
        blank=True,
        help_prefix=_(
            'Visualize your plan.'
        ),
    )
    topics = TopicField()
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

    @property
    def administrative_district(self):
        return self.district

    @property
    def topic_names(self):
        if hasattr(settings, 'A4_PROJECT_TOPICS'):
            choices = dict(settings.A4_PROJECT_TOPICS)
            return [choices[topic] for topic in self.topics]
        return []

    @cached_property
    def published_projects(self):
        return self.projects.filter(
            is_draft=False, is_public=True, is_archived=False)

    @cached_property
    def participation_string(self):
        project_list = self.published_projects.values_list('id', flat=True)
        phases_in_plan = Phase.objects\
            .select_related('module__project')\
            .filter(module__project_id__in=project_list)\
            .order_by('-start_date')

        if phases_in_plan.active_phases():
            return _('running')

        future_phases_with_start_date = phases_in_plan.future_phases()\
            .exclude(start_date__isnull=True)

        if future_phases_with_start_date:
            future_phase = future_phases_with_start_date.first()
            return _('starts at {}').format(future_phase.start_date.date())

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('meinberlin_plans:plan-detail',
                       kwargs=dict(pk='{:05d}'.format(self.pk),
                                   year=self.created.year))

    def save(self, *args, **kwargs):
        self.description = transforms.clean_html_field(self.description)
        super().save(*args, **kwargs)
