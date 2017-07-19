import json

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.forms.widgets import Widget
from django.template import loader

from apps.maps.models import MapPreset
from apps.maps.models import MapPresetCategory


class MapChoosePolygonWithPresetWidget(Widget):

    class Media:
        js = (
            staticfiles_storage.url('leaflet.js'),
            staticfiles_storage.url('leaflet.draw.js'),
            staticfiles_storage.url(
                'meinberlin_maps/map_choose_polygon_with_preset.js'
            )
        )
        css = {'all': [
            staticfiles_storage.url('leaflet.css'),
            staticfiles_storage.url('leaflet.draw.css'),
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
