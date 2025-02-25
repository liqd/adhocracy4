import json
from collections import OrderedDict


class GeoJsonPointMixin:
    """
    A mixin that processes GeoJSON point data for compatibility with GeoDjango models.

    Classes using this mixin must define a `Meta` class with a `geo_field` attribute,
    specifying the name of the model field that stores the point data.

    Additionally, if `get_properties` returns a non-empty dictionary, the corresponding
    GeoJSON properties are extracted and mapped to the specified model fields.
    """

    def get_properties(self):
        """
        Defines a mapping of GeoJSON properties to model fields.

        Returns:
            dict: A dictionary where keys are GeoJSON property names and values are
                  the corresponding model field names. If a model field name is identical
                  to the GeoJSON property name, its value can be set to None.
        """
        return {}

    def unpack_geojson(self, data):
        """
        Extracts and reformats GeoJSON point data for use in a GeoDjango model.

        Args:
            data (dict): A dictionary containing GeoJSON data, including a point field
                         specified by `Meta.geo_field`.

        Returns:
            dict: A modified version of `data` where:
                - The geometry of the GeoJSON point is extracted and stored in `geo_field`.
                - Relevant GeoJSON properties are mapped to their corresponding model fields,
                  based on the mapping defined in `get_properties`.
        """
        if self.Meta.geo_field and self.Meta.geo_field in data:
            geo_field = data[self.Meta.geo_field]
            if geo_field:
                if isinstance(geo_field, dict):
                    point = geo_field
                else:
                    point = json.loads(geo_field)
                data = data.copy()

                if "geometry" in point:
                    data[self.Meta.geo_field] = json.dumps(point["geometry"])

                properties = self.get_properties()
                if "properties" in point:
                    point_properties = point["properties"]

                    for prop, mapping in properties.items():
                        if prop in point_properties:
                            field = mapping if mapping else prop
                            data[field] = point_properties[prop]
        return data


class PointFormMixin(GeoJsonPointMixin):

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if "data" in kwargs:
            kwargs["data"] = self.unpack_geojson(kwargs["data"])

        return kwargs


class PointSerializerMixin(GeoJsonPointMixin):
    """Serializes a GeoDjango Point field into a geojson feature. Requires the field
    `geo_field` on the Meta class of the serializer to be set to the name of the
    model field containing the point.
    """

    def to_internal_value(self, data):
        data = self.unpack_geojson(data)
        return super().to_internal_value(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.Meta.geo_field and self.Meta.geo_field in data:
            if data[self.Meta.geo_field]:
                feature = OrderedDict()
                feature["type"] = "Feature"
                feature["geometry"] = data[self.Meta.geo_field]

                props = OrderedDict()
                properties = self.get_properties()
                for prop, mapping in properties.items():
                    field = mapping if mapping else prop
                    if hasattr(instance, field):
                        props[prop] = getattr(instance, field)

                if props:
                    feature["properties"] = props
                data[self.Meta.geo_field] = feature
        return data
