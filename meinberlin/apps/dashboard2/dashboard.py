from django.utils.translation import ugettext_lazy as _

from . import DashboardComponent
from . import content
from . import views
from .apps import Config


class ProjectBasicComponent(DashboardComponent):
    app_label = Config.label
    label = 'basic'
    identifier = 'basic'

    def get_menu_label(self, project):
        return _('Basic settings')

    def get_view(self):
        return views.ProjectBasicComponentView.as_view()


class ProjectInformationComponent(DashboardComponent):
    app_label = Config.label
    label = 'information'
    identifier = 'information'

    def get_menu_label(self, project):
        return _('Information')

    def get_view(self):
        return views.ProjectInformationComponentView.as_view()


class ModuleBasicComponent(DashboardComponent):
    app_label = Config.label
    label = 'phases'
    identifier = 'module_basic'

    def get_menu_label(self, module):
        return _('Basic information')

    def get_view(self):
        return views.ModuleBasicComponentView.as_view()


class ModulePhasesComponent(DashboardComponent):
    app_label = Config.label
    label = 'phases'
    identifier = 'phases'

    def get_menu_label(self, module):
        return _('Phases')

    def get_view(self):
        return views.ModulePhasesComponentView.as_view()


content.register_project(ProjectBasicComponent())
content.register_project(ProjectInformationComponent())
content.register_module(ModuleBasicComponent())
content.register_module(ModulePhasesComponent())
