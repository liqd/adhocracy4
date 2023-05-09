import json

from django.conf import settings
from django.forms.widgets import Widget
from django.template import loader

from meinberlin.apps.maps.models import MapPreset
from meinberlin.apps.maps.models import MapPresetCategory


class MapChoosePolygonWithPresetWidget(Widget):
    class Media:
        js = ("a4maps_choose_polygon.js",)

        css = {"all": ["a4maps_choose_polygon.css"]}

    def get_presets(self, category):
        presets = MapPreset.objects.filter(category=category)

        return [
            {"name": preset.name, "polygon": json.dumps(preset.polygon)}
            for preset in presets
        ]

    def render(self, name, value, attrs, renderer=None):
        presets_uncategorized = self.get_presets(None)
        preset_categories = [
            (category.name, self.get_presets(category))
            for category in MapPresetCategory.objects.all()
        ]

        use_vector_map = 0
        mapbox_token = ""
        omt_token = ""
        attribution = ""

        if hasattr(settings, "A4_MAP_ATTRIBUTION"):
            attribution = settings.A4_MAP_ATTRIBUTION

        if hasattr(settings, "A4_USE_VECTORMAP") and settings.A4_USE_VECTORMAP:
            use_vector_map = 1

        if hasattr(settings, "A4_MAPBOX_TOKEN"):
            mapbox_token = settings.A4_MAPBOX_TOKEN

        if hasattr(settings, "A4_OPENMAPTILES_TOKEN"):
            omt_token = settings.A4_OPENMAPTILES_TOKEN

        context = {
            "baseurl": settings.A4_MAP_BASEURL,
            "usevectormap": use_vector_map,
            "mapbox_token": mapbox_token,
            "omt_token": omt_token,
            "attribution": attribution,
            "bbox": json.dumps(settings.A4_MAP_BOUNDING_BOX),
            "name": name,
            "polygon": value,
            "presets_uncategorized": presets_uncategorized,
            "preset_categories": preset_categories,
        }

        return loader.render_to_string(
            "meinberlin_maps/map_choose_polygon_with_preset_widget.html", context
        )
