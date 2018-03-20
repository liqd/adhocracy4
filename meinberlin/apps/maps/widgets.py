import json

from django.conf import settings
from django.forms.widgets import Widget
from django.template import loader

from meinberlin.apps.maps.models import MapPreset
from meinberlin.apps.maps.models import MapPresetCategory


class MapChoosePolygonWithPresetWidget(Widget):

    class Media:
        js = (
            'leaflet.js',
            'map_choose_polygon_with_preset.js'
        )
        css = {'all': [
            'leaflet.css',
            'map_choose_polygon_with_preset.css',
        ]}

    def get_presets(self, category):
        presets = MapPreset.objects.filter(category=category)

        return [{
            'name': preset.name,
            'polygon': json.dumps(preset.polygon)
        } for preset in presets]

    def render(self, name, value, attrs):
        presets_uncategorized = self.get_presets(None)
        preset_categories = [
            (category.name, self.get_presets(category))
            for category in MapPresetCategory.objects.all()
        ]

        context = {
            'baseurl': settings.A4_MAP_BASEURL,
            'attribution': settings.A4_MAP_ATTRIBUTION,
            'bbox': json.dumps(settings.A4_MAP_BOUNDING_BOX),
            'name': name,
            'polygon': value,
            'presets_uncategorized': presets_uncategorized,
            'preset_categories': preset_categories
        }

        return loader.render_to_string(
            'meinberlin_maps/map_choose_polygon_with_preset_widget.html',
            context
        )
