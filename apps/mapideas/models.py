from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from adhocracy4.maps import fields as map_fields

from apps.ideas import models as idea_models


class AbstractMapIdea(idea_models.AbstractIdea):
    point = map_fields.PointField(
        verbose_name=_('Where can your idea be located on a map?'),
        help_text=_('Click inside marked area to set a marker. '
                    'Drag and drop marker to change place.'))

    class Meta:
        abstract = True


class MapIdea(AbstractMapIdea):

    def get_absolute_url(self):
        return reverse('mapideas:idea-detail', args=[str(self.slug)])
