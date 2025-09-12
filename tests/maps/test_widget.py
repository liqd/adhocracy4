import json
from unittest.mock import patch

import pytest
from django.test import override_settings
from django.utils.html import format_html

from adhocracy4.maps import widgets


@override_settings(A4_MAP_BASEURL="https://{s}.tile.openstreetmap.org/")
@override_settings(A4_MAP_ATTRIBUTION='<a href="example.com">attribution</a>')
@pytest.mark.django_db
def test_choose_point_widget_with_geos_point(area_settings, geos_point, geojson_point):
    widget = widgets.MapChoosePointWidget(area_settings.polygon)
    widget.geo_json_properties = {"str_name": "Unknown Road"}
    with patch("django.contrib.staticfiles.finders.find") as mock_find:
        mock_find.return_value = "path/to/a4maps_choose_point.js"
        html = widget.render("test_filter", geos_point, attrs={"id": "test_id"})
        expected = format_html(
            """<div
    style="height: 300px;"
    data-map="choose_point"
    data-baseurl="{baseurl}"
    data-usevectormap="{usevectormap}"
    data-mapbox-token=""
    data-omt-token=""
    data-attribution="{attribution}"
    data-name="{name}"
    data-point="{point}"
    data-polygon="{polygon}"
></div>

<input id="id_test_filter" type="hidden" name="test_filter" value="{point}">
""",
            baseurl="https://{s}.tile.openstreetmap.org/",
            usevectormap=0,
            polygon=json.dumps(area_settings.polygon),
            point=json.dumps(geojson_point),
            attribution='<a href="example.com">attribution</a>',
            name="test_filter",
        )
        assert widget.polygon == area_settings.polygon
        assert html == expected
