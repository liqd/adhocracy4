import json
import re
from html import unescape

import pytest
from django.conf import settings
from django.test.utils import override_settings
from django.utils.html import escape

from adhocracy4.maps_react.utils import get_map_settings
from adhocracy4.test import helpers


@override_settings(
    A4_MAP_ATTRIBUTION="attribution",
    A4_MAP_BASEURL="https://{s}.tile.openstreetmap.org/",
)
def test_get_map_settings_with_settings():
    result = get_map_settings(test_setting="value", empty="")
    assert result["attribution"] == "attribution"
    assert result["test_setting"] == "value"
    assert result["baseUrl"] == "https://{s}.tile.openstreetmap.org/"
    assert "empty" not in result


@override_settings(A4_MAP_BASEURL="https://{s}.tile.openstreetmap.org/")
@override_settings(A4_MAP_ATTRIBUTION='<a href="example.com">attribution</a>')
@pytest.mark.django_db
def test_map_display_point(area_settings):
    point = {"test": [1, 2]}

    template = "{% load maps_tags %}{% map_display_point point polygon %}"
    context = {"point": point, "polygon": area_settings.polygon}

    expected = (
        r"^<div"
        r' style="height: 300px"'
        r' data-map="display_point"'
        r' data-baseurl="{baseurl}"'
        r' data-usevectormap="0"'
        r' data-mapbox-token=""'
        r' data-omt-token=""'
        r' data-attribution="{attribution}"'
        r' data-point="(?P<point>{{.+}})"'
        r' data-polygon="(?P<polygon>{{.+}})"'
        r' data-pin-src="null"'
        r"></div>$"
    ).format(
        baseurl=escape(settings.A4_MAP_BASEURL),
        attribution=escape(settings.A4_MAP_ATTRIBUTION),
    )

    match = re.match(expected, helpers.render_template(template, context))
    assert match
    _point = match.group("point")
    assert json.loads(unescape(_point)) == point
    _polygon = match.group("polygon")
    assert json.loads(unescape(_polygon)) == area_settings.polygon
