from django.views import generic

from adhocracy4.projects.mixins import ProjectMixin
from meinberlin.apps.dashboard2 import mixins

from . import models


class AdminLogProjectDashboardView(ProjectMixin,
                                   mixins.DashboardBaseMixin,
                                   mixins.DashboardComponentMixin,
                                   generic.ListView):
    model = models.LogEntry
    template_name = 'meinberlin_adminlog/project_adminlog.html'
    permission_required = 'a4projects.change_project'
    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().filter(project=self.project)

    def get_permission_object(self):
        return self.project
