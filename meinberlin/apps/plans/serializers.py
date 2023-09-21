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
    subtype = serializers.ReadOnlyField(default="plan")
    tile_image = serializers.SerializerMethodField()
    tile_image_alt_text = serializers.SerializerMethodField()
    tile_image_copyright = serializers.SerializerMethodField()
    type = serializers.ReadOnlyField(default="plan")
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

    def get_url(self, plan: Plan) -> str:
        return plan.get_absolute_url()

    def get_published_projects_count(self, plan: Plan):
        return plan.published_projects.count()

    def get_participation_string(self, plan: Plan) -> str:
        return plan.get_status_display()

    def get_participation_active(self, plan: Plan) -> bool:
        return not bool(plan.status)

    def get_tile_image(self, plan: Plan) -> str:
        if plan.tile_image:
            return get_thumbnailer(plan.tile_image)["project_tile"].url
        elif plan.image:
            return get_thumbnailer(plan.image)["project_tile"].url
        else:
            return ""

    def get_tile_image_alt_text(self, plan: Plan) -> str:
        if plan.tile_image:
            return plan.tile_image_alt_text
        elif plan.image_alt_text:
            return plan.image_alt_text
        else:
            return ""

    def get_tile_image_copyright(self, plan: Plan) -> str:
        if plan.tile_image:
            return plan.tile_image_copyright
        elif plan.image_copyright:
            return plan.image_copyright
