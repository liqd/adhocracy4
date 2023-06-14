from functools import lru_cache

from django.utils.translation import gettext as _

from meinberlin.apps.projectcontainers.models import ProjectContainer
from meinberlin.apps.projects.serializers import ProjectSerializer


class ProjectContainerSerializer(ProjectSerializer):
    class Meta:
        model = ProjectContainer
        fields = [
            "type",
            "subtype",
            "title",
            "url",
            "organisation",
            "tile_image",
            "tile_image_alt_text",
            "tile_image_copyright",
            "point",
            "point_label",
            "cost",
            "district",
            "topics",
            "access",
            "status",
            "participation_string",
            "participation_active",
            "participation",
            "description",
            "future_phase",
            "active_phase",
            "past_phase",
            "plan_url",
            "plan_title",
            "published_projects_count",
            "created_or_modified",
        ]

    @lru_cache(maxsize=1)
    def _get_participation_status_project(self, instance):
        if instance.active_project_count > 0:
            return _("running"), True
        elif instance.future_project_count > 0:
            return _("starts in the future"), True
        else:
            return _("done"), False

    def get_url(self, instance):
        return instance.get_absolute_url()

    def get_type(self, instance):
        return "project"

    def get_subtype(self, instance):
        return "container"

    def get_status(self, instance):
        string, status = self._get_participation_status_project(instance)
        return not bool(status)

    def get_future_phase(self, instance):
        return False

    def get_active_phase(self, instance):
        return False

    def get_past_phase(self, instance):
        return False

    def get_published_projects_count(self, instance):
        return instance.projectcontainer.total_project_count
