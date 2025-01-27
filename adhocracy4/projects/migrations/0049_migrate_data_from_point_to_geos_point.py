# Generated by Django 4.2.17 on 2025-01-27 15:11

import json
import logging

from django.contrib.gis.geos import GEOSGeometry
from django.db import migrations

logger = logging.getLogger(__name__)


def migrate_project_point_field(apps, schema_editor):
    project = apps.get_model("a4projects", "Project")
    for project in project.objects.all():
        geojson_point = project.point
        if not geojson_point:
            continue
        if not "geometry" in geojson_point:
            logger.warning(
                "error migrating point of project "
                + project.name
                + ": "
                + str(geojson_point)
            )
            continue
        # Existing points have a set of properties (from the address search on the map)
        # They are in German and are never used again. For sake of preserving the data
        # we map them to new english fields on the model
        project.geos_point = GEOSGeometry(json.dumps(geojson_point["geometry"]))
        if "properties" in geojson_point:
            properties = geojson_point["properties"]
            if "strname" in properties:
                project.street_name = properties["strname"]
            if "hsnr" in properties:
                project.house_number = properties["hsnr"]
            if "plz" in properties:
                project.zip_code = properties["plz"]
        project.save()


class Migration(migrations.Migration):

    dependencies = [
        ("a4projects", "0048_project_geos_point_project_house_number_and_more"),
    ]

    operations = [
        migrations.RunPython(
            migrate_project_point_field, reverse_code=migrations.RunPython.noop
        ),
    ]
