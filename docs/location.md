# Migrating from Custom JSONField to GeoDjango PointField

## Overview

In the past we stored geospatial data as GeoJSON within a custom `JSONField`, primarily for representing `Point` locations. While functional for basic storage, this approach lacked spatial query capabilities. To enhance performance and enable geospatial operations, we migrated the `point` field in the `Project` model to Django's `PointField` from GeoDjango.

## Why Migrate?

The key motivations for this migration include:

- **Improved Querying**: `PointField` supports spatial operations such as distance filtering, intersection detection, and bounding box queries directly at the database level.
- **Performance Boost**: Native spatial indexing and operations significantly improve query efficiency compared to handling geospatial data as raw JSON.

## GeoDjango Enhancements

### Spatial Queries

With `PointField`, we can now efficiently perform spatial queries. For example, retrieving projects within a 10km radius of a given location:

```python
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

point = Point(-104.9903, 39.7392)  # Example coordinates (longitude, latitude)
nearby_projects = Project.objects.filter(location__distance_lte=(point, 10000))  # 10km range
```

### Point Validation and Conversion

To enhance data validation and handling, we introduced:

- **`PointInPolygonValidator`**: Ensures points fall within a predefined polygon, validating both form and serializer inputs.
- **`PointFormMixin` & `PointSerializerMixin`**: These mixins facilitate conversion between a GeoDjango `Point` object and a GeoJSON representation, streamlining data transformations between the database and API layers. They also enable mapping GeoJSON properties to model fields and vice versa for seamless serialization.

## Retaining JSONField for Other Use Cases

While we migrated `Project.point` to `PointField`, we continue using `JSONField` where complex GeoJSON structures (such as polygons or metadata) are required.

**Future Considerations:** We should evaluate migrating other fields currently using `JSONField` to appropriate GIS field types for improved performance and spatial query support.

For further details or troubleshooting, refer to the [GeoDjango documentation](https://docs.djangoproject.com/en/stable/ref/contrib/gis/) or contact the development team.
