from django.utils.translation import ugettext_lazy as _

from adhocracy4.modules import models as module_models

from .fields import MultiPolygonField
from .widgets import MapChoosePolygonWidget


class AreaSettings(module_models.AbstractSettings):
    polygon = MultiPolygonField(
        verbose_name=_('Polygon'),
        help_text=_('Please draw an area on the map.')
    )

    @staticmethod
    def widgets():
        return {
            'polygon': MapChoosePolygonWidget
        }
