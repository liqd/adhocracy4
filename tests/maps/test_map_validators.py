import json

import pytest
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.forms import ValidationError

from adhocracy4.maps.validators import PointInPolygonValidator


@pytest.mark.django_db
def test_point_in_polygon_validator_valid_point():
    polygon = GEOSGeometry(
        json.dumps(settings.BERLIN_POLYGON["features"][0]["geometry"])
    )
    validator = PointInPolygonValidator(polygon=polygon)

    # point within the berlin polygon
    geojson_point = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [13.411924777644563, 52.499598134440944],
        },
    }
    geos_point = GEOSGeometry(json.dumps(geojson_point["geometry"]))
    validator(geos_point)


@pytest.mark.django_db
def test_point_in_polygon_validator_invalid_point():
    polygon = GEOSGeometry(
        json.dumps(settings.BERLIN_POLYGON["features"][0]["geometry"])
    )
    validator = PointInPolygonValidator(polygon=polygon)

    # point outside the berlin polygon
    geojson_point = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [13.459894, 51.574425]},
    }
    geos_point = GEOSGeometry(json.dumps(geojson_point["geometry"]))
    with pytest.raises(ValidationError):
        validator(geos_point)
