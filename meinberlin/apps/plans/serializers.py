from easy_thumbnails.files import get_thumbnailer
from rest_framework import serializers

from meinberlin.apps.projects.serializers import CommonFields

from .models import Plan


class PlanSerializer(serializers.ModelSerializer, CommonFields):
    created_or_modified = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    organisation = serializers.SerializerMethodField()
    participation_active = serializers.SerializerMethodField()
    participation_string = serializers.SerializerMethodField()
    point = serializers.SerializerMethodField()
    published_projects_count = serializers.SerializerMethodField()
    subtype = serializers.SerializerMethodField()
    tile_image = serializers.SerializerMethodField()
    tile_image_alt_text = serializers.SerializerMethodField()
    tile_image_copyright = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = [
            "cost",
            "created_or_modified",
            "district",
            "organisation",
            "participation",
            "participation_active",
            "participation_string",
            "point",
            "point_label",
            "published_projects_count",
            "status",
            "subtype",
            "tile_image",
            "tile_image_alt_text",
            "tile_image_copyright",
            "title",
            "topics",
            "type",
            "url",
        ]

    def get_subtype(self, instance):
        return "plan"

    def _get_participation_status_plan(self, item):
        return item.get_status_display(), not bool(item.status)

    def get_type(self, instance):
        return "plan"

    def get_url(self, instance):
        return instance.get_absolute_url()

    def get_published_projects_count(self, instance):
        return instance.published_projects.count()

    def get_participation_string(self, instance):
        (
            participation_string,
            participation_active,
        ) = self._get_participation_status_plan(instance)
        return str(participation_string)

    def get_participation_active(self, instance):
        (
            participation_string,
            participation_active,
        ) = self._get_participation_status_plan(instance)
        return participation_active

    def get_tile_image(self, instance):
        image_url = ""
        if instance.tile_image:
            image = get_thumbnailer(instance.tile_image)["project_tile"]
            image_url = image.url
        elif instance.image:
            image = get_thumbnailer(instance.image)["project_tile"]
            image_url = image.url
        return image_url

    def get_tile_image_alt_text(self, instance):
        if instance.tile_image:
            return instance.tile_image_alt_text
        elif instance.image_alt_text:
            return instance.image_alt_text
        else:
            return None

    def get_tile_image_copyright(self, instance):
        if instance.tile_image:
            return instance.tile_image_copyright
        elif instance.image_copyright:
            return instance.image_copyright
        else:
            return None
