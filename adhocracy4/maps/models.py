from adhocracy4.modules import models as module_models

from .fields import MultiPolygonField
from .widgets import MapChoosePolygonWidget


class AreaSettings(module_models.AbstractSettings):
    polygon = MultiPolygonField()

    @staticmethod
    def widgets():
        return {
            'polygon': MapChoosePolygonWidget
        }
