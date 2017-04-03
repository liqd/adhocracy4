from django.core import validators as django_validators
from django.utils.translation import ugettext_lazy as _
from jsonfield.fields import JSONField, JSONFormField


class GeoJSONFormField(JSONFormField):

    def to_python(self, value):
        empty_featureset = '{"type":"FeatureCollection","features":[]}'
        if (value not in django_validators.EMPTY_VALUES and not
                value == empty_featureset):
            return super().to_python(value)
        else:
            return None


class GeoJSONField(JSONField):
    description = _("Geometry as GeoJSON")
    form_class = GeoJSONFormField
    dim = 2
    geom_type = 'GEOMETRY'

    def formfield(self, **kwargs):
        error_messages = {'required': self.required_message}
        error_messages.update(kwargs.get('error_messages', {}))
        kwargs['error_messages'] = error_messages
        return super(GeoJSONField, self).formfield(**kwargs)


class GeometryField(GeoJSONField):
    pass


class PointField(GeometryField):
    geom_type = 'POINT'
    required_message = _('Please add a Marker on the map')


class MultiPolygonField(GeoJSONField):
    geom_type = 'MULTIPOLYGON'
    required_message = _('Please draw a Polygon on the map')
