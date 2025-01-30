import json
from collections import OrderedDict


class GeoJsonPointMixin:
    """Mixin which unpacks a geojson point into a format which can be saved by GeoDjango.
    Classes using this mixin need to define a Meta class with a field `geo_field` which has the name of the point field.
    Additionally, if `get_properties` returns a non-empty list, the matching geojson properties are extracted to model fields.
    """

    def get_properties(self):
        return []

    def unpack_geojson(self, data):
        if self.Meta.geo_field and self.Meta.geo_field in data:
            geo_field = data[self.Meta.geo_field]
            point = json.loads(geo_field)
            data = data.copy()
            if "geometry" in point:
                data[self.Meta.geo_field] = json.dumps(point["geometry"])
            properties = self.get_properties()
            if "properties" in point:
                for property in properties:
                    if property in point["properties"]:
                        data[property] = point["properties"][property]
        return data


class PointFormMixin(GeoJsonPointMixin):

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if "data" in kwargs:
            data = self.unpack_geojson(kwargs["data"])
            kwargs["data"] = data
        return kwargs


class PointSerializerMixin(GeoJsonPointMixin):
    """Serializes a GeoDjango Point field into a geojson feature. Requires the field `geo_field`
    on the Meta class of the serializer to be set to the name of the model field containing the point.
    """

    def to_internal_value(self, data):
        data = self.unpack_geojson(data)
        return super().to_internal_value(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.Meta.geo_field and self.Meta.geo_field in data:
            feature = OrderedDict()
            feature["type"] = "Feature"
            feature["geometry"] = data[self.Meta.geo_field]
            props = OrderedDict()
            properties = self.get_properties()
            for property in properties:
                if hasattr(instance, property):
                    props[property] = getattr(instance, property)
            if props:
                feature["properties"] = props
            data[self.Meta.geo_field] = feature
        return data

    def get_properties(self):
        return []
