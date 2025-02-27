import json
from collections import OrderedDict


class GeoJsonPointMixin:
    """
    Mixin to process GeoJSON point data for compatibility with GeoDjango models.

    If `get_geojson_properties()` returns a non-empty dict, the corresponding GeoJSON
    properties will be extracted and mapped to the specified model fields.
    """

    def get_geojson_properties(self):
        """
        Return a mapping of GeoJSON property names to model field names.

        Returns:
            dict: A dictionary where keys are GeoJSON property names and values are the
                  corresponding model field names. Use None if the names are identical.
        Example:
            {"strname": "street_name", "hsnr": "house_number", "plz": "zip_code"}
        """
        return {}

    def map_field_name(self, geojson_property, field_mapping, point_data=None):
        """
        Return the relevant model field name for a given GeoJSON property.

        If point_data is provided and contains a "properties" dictionary, the mapping
        is only applied if the geojson_property exists in those properties; otherwise, None is returned.

        Args:
            geojson_property (str): The GeoJSON property name.
            field_mapping (str or None): The mapped model field name (or None if they are identical).
            point_data (dict, optional): Parsed GeoJSON point data.

        Returns:
            str or None: The model field name if geo_property is found (or if no point_data provided),
                         otherwise None.
        """
        if point_data is not None and "properties" in point_data:
            point_properties = point_data["properties"]
            if geojson_property not in point_properties:
                return None
        return field_mapping if field_mapping else geojson_property

    def map_properties_to_model_fields(self, point_data):
        """
        Extract and map properties from parsed GeoJSON data to model fields.

        Args:
            point_data (dict): A dictionary containing GeoJSON data with a "properties" key.

        Returns:
            OrderedDict: A mapping of model field names to values from the GeoJSON properties.
        """
        extracted = OrderedDict()
        geo_properties = self.get_geojson_properties()
        if "properties" in point_data:
            point_properties = point_data["properties"]

            for geo_prop, mapping in geo_properties.items():
                # Use the helper method to get the relevant field name.
                field_name = self.map_field_name(
                    geo_prop, mapping, point_data=point_data
                )

                if field_name is not None and geo_prop in point_properties:
                    extracted[field_name] = point_properties[geo_prop]

        return extracted

    def extract_instance_properties(self, instance):
        """
        Extract and map properties from a model instance based on the geojson mapping.

        Args:
            instance: A model instance.

        Returns:
            OrderedDict: A mapping of GeoJSON property names to instance attribute values.
        """
        extracted = OrderedDict()
        geo_properties = self.get_geojson_properties()

        for geo_prop, mapping in geo_properties.items():
            field_name = self.map_field_name(geo_prop, mapping, point_data=None)

            if hasattr(instance, field_name):
                extracted[geo_prop] = getattr(instance, field_name)

        return extracted

    def unpack_geojson(self, data):
        """
        Extract and reformat GeoJSON point data for use in a GeoDjango model.

        Args:
            data (dict): Dictionary containing GeoJSON data including the point field,
                         specified by the Meta.geo_field attribute.

        Returns:
            dict: A modified copy of `data` with:
                - The geometry extracted and stored as a JSON string.
                - Mapped GeoJSON properties based on the mapping provided by `get_geojson_properties()`.
        """
        geo_field_name = self.Meta.geo_field
        if geo_field_name and geo_field_name in data:
            geo_field_value = data[geo_field_name]
            if geo_field_value:
                # Parse the geo_field value into a dictionary if necessary.
                if isinstance(geo_field_value, dict):
                    point_data = geo_field_value
                else:
                    point_data = json.loads(geo_field_value)

                # Create a copy to avoid mutating the input data.
                data = data.copy()

                # Extract and update the geometry if present.
                if "geometry" in point_data:
                    data[geo_field_name] = json.dumps(point_data["geometry"])

                # Update data with mapped GeoJSON properties.
                field_properties = self.map_properties_to_model_fields(point_data)
                for field, value in field_properties.items():
                    data[field] = value
        return data


class PointFormMixin(GeoJsonPointMixin):
    """
    Mixin for forms to serialize a GeoDjango point field as valid GeoJSON.

    Classes using this mixin must define a Meta inner class with a `geo_field` attribute,
    which specifies the model field name where the point data is stored.

    """

    def __init__(self, *args, **kwargs):
        # On form submission, extract the geometry from the GeoJSON data.
        # FIXME: This should probably be done in a custom form field's clean() method.
        if "data" in kwargs:
            kwargs["data"] = self.unpack_geojson(kwargs["data"])
        super().__init__(*args, **kwargs)

        # On initial form rendering, pre-populate the widget's geo_json_properties with instance values.
        if "data" not in kwargs:
            geo_properties = self.get_geojson_properties()
            if geo_properties:
                instance = kwargs.get("instance")
                if instance:
                    props = self.extract_instance_properties(instance)
                    if props:
                        self.fields[self.Meta.geo_field].widget.geo_json_properties = (
                            props
                        )


class PointSerializerMixin(GeoJsonPointMixin):
    """
    Mixin for serializers to convert a GeoDjango Point field into a GeoJSON feature.

    The Meta class of the serializer must define `geo_field` as the name of the model field
    containing the point data.
    """

    def to_internal_value(self, data):
        """
        Convert input data to an internal representation by unpacking GeoJSON.
        """
        unpacked_data = self.unpack_geojson(data)
        return super().to_internal_value(unpacked_data)

    def to_representation(self, instance):
        """
        Convert a model instance into a GeoJSON feature representation.
        """
        data = super().to_representation(instance)
        geo_field = self.Meta.geo_field
        if geo_field and geo_field in data and data[geo_field]:
            feature = OrderedDict({"type": "Feature", "geometry": data[geo_field]})

            # Extract properties from the instance.
            properties = self.extract_instance_properties(instance)
            if properties:
                feature["properties"] = properties

            data[geo_field] = feature

        return data
