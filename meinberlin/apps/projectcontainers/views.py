from django.views import generic

from meinberlin.apps.dashboard2 import mixins as dashboard_mixins
from meinberlin.apps.dashboard2.components.forms.views import \
    ProjectComponentFormView

from . import models


class ContainerProjectUpdateView(ProjectComponentFormView):

    model = models.ProjectContainer

    def get_project(self, *args, **kwargs):
        project = super().get_project(*args, **kwargs)
        return project.projectcontainer

    def get_object(self, queryset=None):
        return self.project

    def validate_object_project(self):
        return True

    def validate_object_module(self):
        return True


class ContainerListView(dashboard_mixins.DashboardBaseMixin,
                        generic.ListView):
    model = models.ProjectContainer
    paginate_by = 12
    template_name = 'meinberlin_projectcontainers/container_list.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'

    def get_queryset(self):
        return super().get_queryset().filter(
            organisation=self.organisation
        )
