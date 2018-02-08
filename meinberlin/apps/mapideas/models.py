from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from adhocracy4.maps import fields as map_fields
from meinberlin.apps.ideas import models as idea_models


class AbstractMapIdea(idea_models.AbstractIdea):
    point = map_fields.PointField(
        verbose_name=_('Where can your idea be located on a map?'),
        help_text=_('Click inside marked area on the map to set a marker. '
                    'Drag and drop the marker to change its place. '
                    'Alternatively you can use the search field to search '
                    'for an address.'))

    point_label = models.CharField(
        blank=True,
        default='',
        max_length=255,
        verbose_name=_('Label of the ideas location'),
        help_text=_('This could be an address or the name of a landmark.'),
    )

    class Meta:
        abstract = True


class MapIdea(AbstractMapIdea):

    def get_absolute_url(self):
        return reverse('meinberlin_mapideas:mapidea-detail',
                       kwargs=dict(pk='{:05d}'.format(self.pk),
                                   year=self.created.year))

    class Meta:
        ordering = ['-created']
