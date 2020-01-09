import json
import re
from html import unescape

import pytest
from django.conf import settings
from django.test.utils import override_settings
from django.utils.html import escape

from adhocracy4.maps.templatetags import maps_tags
from adhocracy4.test import helpers
from tests.helpers import pytest_regex


def test_get_points_empty():
    items = []

    result = json.loads(maps_tags.get_points(items))

    assert result == {
        'type': 'FeatureCollection',
        'features': []
    }


@pytest.mark.django_db
def test_get_points_one(location_factory):
    items = [
        location_factory()
    ]

    result = json.loads(maps_tags.get_points(items))

    assert result == {
        'type': 'FeatureCollection',
        'features': [{
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [1.0, 1.0]
            },
            'properties': {
                'name': '',
                'slug': 'location',
                'url': pytest_regex('^/location/[0-9]*/$'),
                'image': '',
                'category_icon': '',
                'comments_count': '',
                'positive_rating_count': '',
                'negative_rating_count': ''
            }
        }]
    }


@pytest.mark.django_db
def test_get_points_two(location_factory):
    items = [
        location_factory(),
        location_factory()
    ]

    result = json.loads(maps_tags.get_points(items))

    assert len(result['features']) == 2


@pytest.mark.django_db
def test_get_points_with_properties(location_factory):
    items = [
        location_factory()
    ]

    items[0].comment_count = 2
    items[0].positive_rating_count = 3
    items[0].negative_rating_count = 4

    result = json.loads(maps_tags.get_points(items))

    assert result == {
        'type': 'FeatureCollection',
        'features': [{
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [1.0, 1.0]
            },
            'properties': {
                'name': '',
                'slug': 'location',
                'url': pytest_regex('^/location/[0-9]*/$'),
                'image': '',
                'category_icon': '',
                'comments_count': 2,
                'positive_rating_count': 3,
                'negative_rating_count': 4
            }
        }]
    }


@override_settings(A4_MAP_BASEURL='https://{s}.tile.openstreetmap.org/')
@override_settings(A4_MAP_ATTRIBUTION='<a href="example.com">attribution</a>')
@pytest.mark.django_db
def test_map_display_points(area_settings, location_factory):
    items = [
        location_factory()
    ]

    points = {
        "type": "FeatureCollection",
        "features": [
            {
                "properties": {
                    "name": "",
                    "comments_count": "",
                    "url": pytest_regex('^/location/[0-9]*/$'),
                    "positive_rating_count": "",
                    "slug": "location",
                    "image": "",
                    "category_icon": "",
                    "negative_rating_count": ""},
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [1.0, 1.0]
                }
            }
        ]
    }

    template = '{% load maps_tags %}{% map_display_points items polygon %}'
    context = {'items': items, 'polygon': area_settings.polygon}

    expected = (
        r'^<div'
        r' style="height: 300px"'
        r' data-map="display_points"'
        r' data-baseurl="{baseurl}"'
        r' data-usevectormap="0"'
        r' data-mapbox-token=""'
        r' data-omt-token=""'
        r' data-attribution="{attribution}"'
        r' data-points="(?P<points>{{.+}})"'
        r' data-polygon="(?P<polygon>{{.+}})"'
        ' data-hide-ratings="false"'
        r'></div>$'
    ).format(baseurl=escape(settings.A4_MAP_BASEURL),
             attribution=escape(settings.A4_MAP_ATTRIBUTION))

    match = re.match(expected, helpers.render_template(template, context))
    assert match
    _points = match.group('points')
    assert json.loads(unescape(_points)) == points
    _polygon = match.group('polygon')
    assert json.loads(unescape(_polygon)) == area_settings.polygon


@override_settings(A4_MAP_BASEURL='https://{s}.tile.openstreetmap.org/')
@override_settings(A4_MAP_ATTRIBUTION='<a href="example.com">attribution</a>')
@pytest.mark.django_db
def test_map_display_point(area_settings):
    point = {'test': [1, 2]}

    template = '{% load maps_tags %}{% map_display_point point polygon %}'
    context = {'point': point, 'polygon': area_settings.polygon}

    expected = (
        r'^<div'
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
        r'></div>$'
    ).format(baseurl=escape(settings.A4_MAP_BASEURL),
             attribution=escape(settings.A4_MAP_ATTRIBUTION))

    match = re.match(expected, helpers.render_template(template, context))
    assert match
    _point = match.group('point')
    assert json.loads(unescape(_point)) == point
    _polygon = match.group('polygon')
    assert json.loads(unescape(_polygon)) == area_settings.polygon
