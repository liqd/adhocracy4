import json

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.forms.widgets import Widget
from django.template import loader


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

    def render(self, name, value, attrs):

        context = {
            'baseurl': settings.A4_MAP_BASEURL,
            'attribution': settings.A4_MAP_ATTRIBUTION,
            'bbox': json.dumps(settings.A4_MAP_BOUNDING_BOX),
            'name': name,
            'polygon': value
        }

        return loader.render_to_string(
            'meinberlin_maps/map_choose_polygon_with_preset_widget.html',
            context
        )
