import json

import pytest
from django.contrib.gis.geos import GEOSGeometry
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_gis.fields import GeometryField

from adhocracy4.maps.mixins import PointSerializerMixin


class TestPointSerializer(PointSerializerMixin, serializers.Serializer):
    point = GeometryField()
    street_name = serializers.CharField(required=False)

    class Meta:
        geo_field = "point"


@pytest.mark.django_db
def test_valid_point_correctly_serialized_to_internal_value():
    geojson_point = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [13.411924777644563, 52.499598134440944],
        },
    }
    gis_point = GEOSGeometry(json.dumps(geojson_point["geometry"]))
    serializer = TestPointSerializer()
    point = serializer.to_internal_value(data={"point": json.dumps(geojson_point)})
    assert point["point"] == gis_point


@pytest.mark.django_db
def test_valid_point_with_properties_to_internal_value():
    geojson_point = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [13.411924777644563, 52.499598134440944],
        },
        "properties": {"street_name": "Unknown Road"},
    }
    gis_point = GEOSGeometry(json.dumps(geojson_point["geometry"]))
    serializer = TestPointSerializer()
    serializer.get_properties = lambda: ["street_name"]
    data = serializer.to_internal_value(data={"point": json.dumps(geojson_point)})
    assert data["point"] == gis_point
    assert data["street_name"] == "Unknown Road"


@pytest.mark.django_db
def test_invalid_point_to_internal_value_throws_error():
    geojson_point = {
        "type": "Feature",
    }
    serializer = TestPointSerializer()
    with pytest.raises(ValidationError):
        serializer.to_internal_value(data={"point": json.dumps(geojson_point)})


@pytest.mark.django_db
def test_valid_point_to_representation():
    geojson_point = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [13.411924777644563, 52.499598134440944],
        },
    }

    class FakeSerializer:
        def to_representation(self, instance):
            return {
                "point": {
                    "type": "Point",
                    "coordinates": [13.411924777644563, 52.499598134440944],
                }
            }

    class FakePointSerializer(PointSerializerMixin, FakeSerializer):
        class Meta:
            geo_field = "point"

        def to_representation(self, instance):
            return super().to_representation(instance)

    serializer = FakePointSerializer()
    data = serializer.to_representation(None)
    assert data["point"] == geojson_point
