import json
from unittest.mock import patch

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings
from django.utils.html import format_html

from adhocracy4.maps_react import widgets


@override_settings(A4_MAP_BASEURL="https://{s}.tile.openstreetmap.org/")
@override_settings(A4_MAP_ATTRIBUTION='<a href="example.com">attribution</a>')
@pytest.mark.django_db
def test_choose_point_widget_throws(area_settings):
    widget = widgets.MapChoosePointWidget(area_settings.polygon)
    with pytest.raises(ImproperlyConfigured):
        widget.render("test_filter", "test_val1", attrs={"id": "test_id"})


@override_settings(A4_MAP_BASEURL="https://{s}.tile.openstreetmap.org/")
@override_settings(A4_MAP_ATTRIBUTION='<a href="example.com">attribution</a>')
@pytest.mark.django_db
def test_choose_point_widget(area_settings):
    widget = widgets.MapChoosePointWidget(area_settings.polygon)
    with patch("django.contrib.staticfiles.finders.find") as mock_find:
        mock_find.return_value = "path/to/a4maps_choose_point.js"
        html = widget.render("test_filter", "test_val1", attrs={"id": "test_id"})
        attrs = {
            "map": {
                "attribution": '<a href="example.com">attribution</a>',
                "useVectorMap": 0,
                "baseUrl": "https://{s}.tile.openstreetmap.org/",
                "polygon": area_settings.polygon,
                "point": "test_val1",
                "name": "test_filter",
            }
        }
        expected = format_html(
            """

<div data-a4-widget="react-choose-point" data-attributes="{attributes}"></div>
<input id="id_test_filter" type="hidden" name="test_filter" value="test_val1">
""",
            attributes=json.dumps(attrs),
        )
        assert widget.polygon == area_settings.polygon
        assert html == expected
