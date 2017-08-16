from django.utils.translation import ugettext_lazy as _

from . import DashboardComponent
from . import content
from . import forms
from . import views
from .apps import Config


class ProjectBasicComponent(DashboardComponent):
    app_label = Config.label
    label = 'basic'
    identifier = 'basic'

    def get_menu_label(self, project):
        return _('Basic settings')

    def get_view(self):
        return views.ProjectComponentFormView.as_view(
            title=_('Edit basic settings'),
            form_class=forms.ProjectBasicForm,
            form_template_name='meinberlin_dashboard2'
                               '/includes/project_basic_form.html'
        )


class ProjectInformationComponent(DashboardComponent):
    app_label = Config.label
    label = 'information'
    identifier = 'information'

    def get_menu_label(self, project):
        return _('Information')

    def get_view(self):
        return views.ProjectComponentFormView.as_view(
            title=_('Edit project information'),
            form_class=forms.ProjectInformationForm,
            form_template_name='meinberlin_dashboard2'
                               '/includes/project_information_form.html',
        )


class ModuleBasicComponent(DashboardComponent):
    app_label = Config.label
    label = 'phases'
    identifier = 'module_basic'

    def get_menu_label(self, module):
        return _('Basic information')

    def get_view(self):
        return views.ModuleComponentFormView.as_view(
            title=_('Edit basic module information'),
            form_class=forms.ModuleBasicForm,
            form_template_name='meinberlin_dashboard2/includes'
                               '/module_basic_form.html'
        )


class ModulePhasesComponent(DashboardComponent):
    app_label = Config.label
    label = 'phases'
    identifier = 'phases'

    def get_menu_label(self, module):
        return _('Phases')

    def get_view(self):
        return views.ModuleComponentFormView.as_view(
            title=_('Edit phases information'),
            form_class=forms.PhaseFormSet,
            form_template_name='meinberlin_dashboard2/includes'
                               '/module_phases_form.html'
        )


content.register_project(ProjectBasicComponent())
content.register_project(ProjectInformationComponent())
content.register_module(ModuleBasicComponent())
content.register_module(ModulePhasesComponent())
