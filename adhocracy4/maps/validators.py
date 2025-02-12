from django.contrib.gis.geos import Polygon
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class PointInPolygonValidator:
    """Validate that the given point is within the polygon, otherwise raise ValidationError."""

    polygon: Polygon = None
    message = _("Point is not inside the specified area")
    code = "invalid"

    def __init__(self, polygon):
        self.polygon = polygon

    def __call__(self, value):
        if not self.polygon.contains(value):
            raise ValidationError(message=self.message, code=self.code)

    def __eq__(self, other):
        return (
            isinstance(other, PointInPolygonValidator)
            and self.message == other.message
            and self.code == other.code
            and self.polygon == other.polygon
        )
