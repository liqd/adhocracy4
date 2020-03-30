from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.modules import models as module_models
from adhocracy4.projects import models as project_models
from adhocracy4.projects.mixins import ProjectMixin

from ... import mixins


class ProjectComponentFormView(ProjectMixin,
                               mixins.DashboardBaseMixin,
                               mixins.DashboardComponentMixin,
                               mixins.DashboardComponentFormSignalMixin,
                               SuccessMessageMixin,
                               generic.UpdateView):

    permission_required = 'a4projects.change_project'
    model = project_models.Project
    template_name = 'a4dashboard/base_form_project.html'
    success_message = _('The project has been updated.')

    # Properties to be set when calling as_view()
    component = None
    title = ''
    form_class = None
    form_template_name = ''

    def get_object(self, queryset=None):
        return self.project

    def get_permission_object(self):
        return self.project


class ModuleComponentFormView(ProjectMixin,
                              mixins.DashboardBaseMixin,
                              mixins.DashboardComponentMixin,
                              mixins.DashboardComponentFormSignalMixin,
                              SuccessMessageMixin,
                              generic.UpdateView):

    permission_required = 'a4projects.change_project'
    model = module_models.Module
    template_name = 'a4dashboard/base_form_module.html'
    success_message = _('The module has been updated.')

    # Properties to be set when calling as_view()
    component = None
    title = ''
    form_class = None
    form_template_name = ''

    def get_object(self, queryset=None):
        return self.module

    def get_permission_object(self):
        return self.project
