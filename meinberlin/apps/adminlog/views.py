from django.views import generic

from adhocracy4.dashboard import mixins
from adhocracy4.projects.mixins import ProjectMixin

from . import models


class AdminLogProjectDashboardView(
    ProjectMixin,
    mixins.DashboardBaseMixin,
    mixins.DashboardComponentMixin,
    generic.ListView,
):
    model = models.LogEntry
    template_name = "meinberlin_adminlog/project_adminlog_dashboard.html"
    permission_required = "a4projects.change_project"
    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().filter(project=self.project)

    def get_permission_object(self):
        return self.project
