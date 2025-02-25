import json

import pytest
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from adhocracy4.maps.mixins import PointSerializerMixin
from adhocracy4.projects.models import Project


class TestPointSerializer(PointSerializerMixin, serializers.ModelSerializer):

    def get_properties(self):
        return {"strname": "street_name"}

    class Meta:
        geo_field = "point"
        fields = ["point", "street_name"]
        model = Project


@pytest.mark.django_db
def test_valid_point_correctly_serialized_to_internal_value(geojson_point, geos_point):
    del geojson_point["properties"]
    serializer = TestPointSerializer()
    data = serializer.to_internal_value(data={"point": json.dumps(geojson_point)})
    assert data["point"].equals(geos_point)
    assert "street_name" not in data


@pytest.mark.django_db
def test_valid_point_as_dict_correctly_serialized_to_internal_value(
    geojson_point, geos_point
):
    del geojson_point["properties"]
    serializer = TestPointSerializer()
    data = serializer.to_internal_value(data={"point": geojson_point})
    assert data["point"].equals(geos_point)
    assert "street_name" not in data


@pytest.mark.django_db
def test_valid_point_with_properties_to_internal_value(geojson_point, geos_point):
    serializer = TestPointSerializer()
    data = serializer.to_internal_value(data={"point": json.dumps(geojson_point)})
    assert data["point"].equals(geos_point)
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
def test_valid_point_to_representation(project, geojson_point, geos_point):
    project.point = geos_point
    project.street_name = geojson_point["properties"]["strname"]
    project.save()

    data = TestPointSerializer(project).data
    assert data["point"] == geojson_point


@pytest.mark.django_db
def test_empty_point_to_representation_doesnt_create_feature(project):
    project.point = None
    project.save()

    data = TestPointSerializer(project).data
    assert not data["point"]
