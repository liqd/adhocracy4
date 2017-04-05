import json

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.forms.widgets import Widget
from django.template import loader


class MapChoosePolygonWidget(Widget):

    class Media:
        js = (staticfiles_storage.url('leaflet.js'),
              staticfiles_storage.url('leaflet.draw.js'),
              staticfiles_storage.url('a4maps/map_choose_polygon.js')
              )
        css = {'all': [
            staticfiles_storage.url('leaflet.css'),
            staticfiles_storage.url('leaflet.draw.css'),
        ]}

    def render(self, name, value, attrs):

        context = {
            'map_url': settings.BASE_MAP,
            'bbox': json.dumps(settings.MAP_BOUNDING_BOX),
            'name': name,
            'polygon': json.dumps(value)
        }

        return loader.render_to_string(
            'a4maps/map_choose_polygon_widget.html',
            context
        )


class MapChoosePointWidget(Widget):

    def __init__(self, polygon, attrs=None):
        self.polygon = polygon
        super().__init__(attrs)

    class Media:
        js = (staticfiles_storage.url('leaflet.js'),
              staticfiles_storage.url('a4maps/map_choose_point.js'),
              )
        css = {'all': [
            staticfiles_storage.url('leaflet.css'),
        ]}

    def render(self, name, value, attrs):

        context = {
            'map_url': settings.BASE_MAP,
            'bbox': json.dumps(settings.MAP_BOUNDING_BOX),
            'name': name,
            'point': json.dumps(value),
            'polygon': json.dumps(self.polygon)
        }

        return loader.render_to_string(
            'a4maps/map_choose_point_widget.html',
            context
        )
