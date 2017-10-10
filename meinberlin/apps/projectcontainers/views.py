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
