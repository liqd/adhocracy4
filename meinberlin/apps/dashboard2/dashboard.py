from django.utils.translation import ugettext_lazy as _

from . import DashboardProjectComponent
from . import content
from . import views
from .apps import Config


class ProjectBasicComponent(DashboardProjectComponent):
    app_label = Config.label
    label = 'basic'
    identifier = 'basic'

    def get_menu_item(self, project):
        return _('Basic settings')

    def get_view(self):
        return views.ProjectBasicComponentView.as_view()


class ProjectInformationComponent(DashboardProjectComponent):
    app_label = Config.label
    label = 'information'
    identifier = 'information'

    def get_menu_item(self, project):
        return _('Information')

    def get_view(self):
        return views.ProjectInformationComponentView.as_view()


content.register_project(ProjectBasicComponent())
content.register_project(ProjectInformationComponent())
