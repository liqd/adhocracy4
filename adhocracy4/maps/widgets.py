import json
from collections import OrderedDict

from django.conf import settings
from django.contrib.gis.geos import Point
from django.forms.widgets import Widget
from django.template import loader


class MapWidgetMixin:
    """
    Mixin to provide common map settings for map-related widgets.
    """

    def get_common_map_context(self):
        """
        Build a dictionary of common map settings from Django settings.

        Returns:
            dict: A dictionary containing map base URL, tokens, attribution,
                  and vector map flag.
        """
        return {
            "baseurl": getattr(settings, "A4_MAP_BASEURL", ""),
            "usevectormap": 1 if getattr(settings, "A4_USE_VECTORMAP", False) else 0,
            "mapbox_token": getattr(settings, "A4_MAPBOX_TOKEN", ""),
            "omt_token": getattr(settings, "A4_OPENMAPTILES_TOKEN", ""),
            "attribution": getattr(settings, "A4_MAP_ATTRIBUTION", ""),
        }


class MapChoosePolygonWidget(MapWidgetMixin, Widget):
    class Media:
        js = ("a4maps_choose_polygon.js",)
        css = {"all": ["a4maps_choose_polygon.css"]}

    def render(self, name, value, attrs, renderer=None):
        # Get the common map context from settings.
        context = self.get_common_map_context()
        # Add polygon-specific context values.
        context.update(
            {
                "bbox": json.dumps(getattr(settings, "A4_MAP_BOUNDING_BOX", [])),
                "name": name,
                "polygon": value,
            }
        )
        return loader.render_to_string("a4maps/map_choose_polygon_widget.html", context)


class MapChoosePointWidget(MapWidgetMixin, Widget):
    geo_json_properties = {}

    def __init__(self, polygon, attrs=None):
        self.polygon = polygon
        super().__init__(attrs)

    class Media:
        js = ("a4maps_choose_point.js",)
        css = {"all": ["a4maps_choose_point.css"]}

    def render(self, name, value, attrs, renderer=None):
        # Get the common map context from settings.
        context = self.get_common_map_context()

        # Process the point value.
        point = value
        if isinstance(point, Point):
            feature = OrderedDict(
                {"type": "Feature", "geometry": json.loads(point.geojson)}
            )
            if self.geo_json_properties:
                feature["properties"] = self.geo_json_properties
            point = json.dumps(feature)

        # Add point-specific context values.
        context.update(
            {
                "name": name,
                "point": point,
                # Use json.dumps because polygon data is passed directly.
                "polygon": json.dumps(self.polygon),
            }
        )

        return loader.render_to_string("a4maps/map_choose_point_widget.html", context)
