import json
import os
import subprocess
import sys

from django.core.management.base import BaseCommand

from meinberlin.apps.maps import models as map_models


class Command(BaseCommand):
    help = "Create map presets for berlin GEO-Data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--gdal-legacy",
            action="store_true",
            dest="gdal_legacy",
            default=False,
            help="GDAL version <= 1.10",
        )

    def handle(self, *args, **options):
        self.is_gdal_legacy = options["gdal_legacy"]
        self._import_districts()
        self._import_regions()

    def _import_districts(self):
        category = self._preset_category("Bezirke - Berlin")
        tmpfile = "/tmp/bezirke.json"
        url = "http://fbinter.stadt-berlin.de/fb/" "wfs/geometry/senstadt/re_bezirke/"
        self._download_geodata(tmpfile, url, "fis:re_bezirke")
        data = json.load(open(tmpfile, "r"))
        for feature in data["features"]:
            district = feature["properties"]["spatial_alias"]
            if not map_models.MapPreset.objects.filter(name=district).exists():
                self._create_map_preset(district, feature, category)
        os.remove(tmpfile)

    def _import_regions(self):
        url = (
            "http://fbinter.stadt-berlin.de/fb/"
            "wfs/geometry/senstadt/re_bezirksregion/"
        )
        tmpfile = "/tmp/bezirksregions.json"
        self._download_geodata(tmpfile, url, "fis:re_bezirksregion")
        data = json.load(open(tmpfile, "r"))
        for feature in data["features"]:
            district = feature["properties"]["BEZNAME"]
            region = feature["properties"]["BZR_NAME"]
            category = self._preset_category(district)
            if not map_models.MapPreset.objects.filter(name=region).exists():
                self._create_map_preset(region, feature, category)
        os.remove(tmpfile)

    def _preset_category(self, name):
        category, _ = map_models.MapPresetCategory.objects.get_or_create(name=name)
        return category

    def _create_map_preset(self, name, feature, category):
        polygon = {"type": "FeatureCollection", "features": [feature]}
        map_preset = map_models.MapPreset(name=name, polygon=polygon, category=category)
        map_preset.save()

    def _download_geodata(self, filename: str, url: str, layer: str):
        try:
            os.remove(filename)
        except OSError:
            pass

        src = "WFS:{}{}".format(url, "?VERSION=1.1.0" if self.is_gdal_legacy else "")
        try:
            print("Trying to download file from {}".format(url))
            subprocess.check_call(
                [
                    "ogr2ogr",
                    "-s_srs",
                    "EPSG:25833",
                    "-t_srs",
                    "WGS84",
                    "-f",
                    "geoJSON",
                    filename,
                    src,
                    layer,
                ]
            )
        except FileNotFoundError as e:
            print("Make sure ogr2ogr is installed and in user PATH.")
            sys.exit(e)
