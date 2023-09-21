from meinberlin.apps.extprojects.models import ExternalProject
from meinberlin.apps.projects.serializers import ProjectSerializer


class ExternalProjectSerializer(ProjectSerializer):
    class Meta:
        model = ExternalProject
        fields = [
            "access",
            "active_phase",
            "cost",
            "created_or_modified",
            "description",
            "district",
            "future_phase",
            "organisation",
            "participation",
            "participation_active",
            "participation_string",
            "past_phase",
            "plan_title",
            "plan_url",
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

    def get_url(self, instance):
        return instance.externalproject.url

    def get_type(self, instance):
        return "project"

    def get_subtype(self, instance):
        return "external"

    def get_published_projects_count(self, instance):
        return 0
