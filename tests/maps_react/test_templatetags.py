import json

import pytest
from django.test import override_settings
from django.utils.html import format_html

from adhocracy4.test.helpers import render_template


@override_settings(A4_MAP_BASEURL="https://{s}.tile.openstreetmap.org/")
@override_settings(A4_MAP_ATTRIBUTION='<a href="example.com">attribution</a>')
@pytest.mark.django_db
def test_react_maps_without_point(rf, area_settings):
    request = rf.get("/")
    attrs = {
        "map": {
            "attribution": '<a href="example.com">attribution</a>',
            "useVectorMap": 0,
            "baseUrl": "https://{s}.tile.openstreetmap.org/",
            "polygon": area_settings.polygon,
            "name": "test",
        }
    }
    expected = format_html(
        '<div data-a4-widget="react-choose-point" data-attributes="{attributes}"></div>',
        attributes=json.dumps(attrs),
    )

    context = {"request": request, "polygon": area_settings.polygon}
    template = '{% load react_maps_tags %}{% react_choose_point polygon=polygon point=point name="test" %}'
    result = render_template(template, context)
    assert result == expected


@override_settings(A4_MAP_BASEURL="https://{s}.tile.openstreetmap.org/")
@override_settings(A4_MAP_ATTRIBUTION='<a href="example.com">attribution</a>')
@pytest.mark.django_db
def test_react_maps_with_point(rf, area_settings):
    request = rf.get("/")
    point = {"test": [1, 2]}

    attrs = {
        "map": {
            "attribution": '<a href="example.com">attribution</a>',
            "useVectorMap": 0,
            "baseUrl": "https://{s}.tile.openstreetmap.org/",
            "polygon": area_settings.polygon,
            "point": point,
            "name": "test",
        }
    }
    expected = format_html(
        '<div data-a4-widget="react-choose-point" data-attributes="{attributes}"></div>',
        attributes=json.dumps(attrs),
    )

    context = {"request": request, "polygon": area_settings.polygon, "point": point}
    template = '{% load react_maps_tags %}{% react_choose_point polygon=polygon point=point name="test" %}'
    result = render_template(template, context)
    assert result == expected
