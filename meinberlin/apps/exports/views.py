from django.views import generic

from adhocracy4.dashboard import mixins as dashboard_mixins
from adhocracy4.projects.mixins import ProjectMixin


class DashboardExportView(ProjectMixin,
                          dashboard_mixins.DashboardBaseMixin,
                          dashboard_mixins.DashboardComponentMixin,
                          generic.TemplateView):
    permission_required = 'a4projects.change_project'

    def get_permission_object(self):
        return self.project
