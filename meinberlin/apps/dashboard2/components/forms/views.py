from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.modules import models as module_models
from adhocracy4.projects import models as project_models
from meinberlin.apps.contrib.views import ProjectContextMixin

from ... import mixins
from ... import signals


class ProjectComponentFormView(ProjectContextMixin,
                               mixins.DashboardBaseMixin,
                               mixins.DashboardComponentMixin,
                               SuccessMessageMixin,
                               generic.UpdateView):

    permission_required = 'a4projects.change_project'
    model = project_models.Project
    template_name = 'meinberlin_dashboard2/base_form_project.html'
    success_message = _('Project successfully updated.')

    # Properties to be set when calling as_view()
    component = None
    title = ''
    form_class = None
    form_template_name = ''

    def get_object(self, queryset=None):
        return self.project

    def get_permission_object(self):
        return self.project

    def form_valid(self, form):
        response = super().form_valid(form)
        signals.project_component_updated.send(sender=None,
                                               project=self.project,
                                               component=self.component,
                                               user=self.request.user)
        return response


class ModuleComponentFormView(ProjectContextMixin,
                              mixins.DashboardBaseMixin,
                              mixins.DashboardComponentMixin,
                              SuccessMessageMixin,
                              generic.UpdateView):

    permission_required = 'a4projects.change_project'
    model = module_models.Module
    template_name = 'meinberlin_dashboard2/base_form_module.html'
    success_message = _('Module successfully updated.')

    # Properties to be set when calling as_view()
    component = None
    title = ''
    form_class = None
    form_template_name = ''

    def get_object(self, queryset=None):
        return self.module

    def get_permission_object(self):
        return self.project

    def form_valid(self, form):
        response = super().form_valid(form)
        signals.module_component_updated.send(sender=None,
                                              module=self.module,
                                              component=self.component,
                                              user=self.request.user)
        return response
