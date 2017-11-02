from autoslug import AutoSlugField
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from adhocracy4.maps import fields as map_fields
from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.projects import models as project_models


class Plan(UserGeneratedContentModel):
    slug = AutoSlugField(populate_from='title', unique=True)
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

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('meinberlin_offlineevents:offlineevent-detail',
                       args=[str(self.slug)])
