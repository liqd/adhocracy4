from django.conf import settings
from django.utils.module_loading import import_string

from .components import DashboardComponent
from .components import components
from .components.forms import ModuleFormComponent
from .components.forms import ModuleFormSetComponent
from .components.forms import ProjectFormComponent

default_app_config = 'adhocracy4.dashboard.apps.Config'

__all__ = ['components', 'DashboardComponent',
           'ModuleFormComponent', 'ModuleFormSetComponent',
           'ProjectFormComponent',
           'get_project_dashboard']


def get_project_dashboard(project):
    key = 'PROJECT_DASHBOARD_CLASS'
    dashboard_settings = getattr(settings, 'A4_DASHBOARD', None)
    if dashboard_settings and key in dashboard_settings:
        dashboard_cls = import_string(dashboard_settings[key])

    else:
        dashboard_cls = ProjectDashboard

    return dashboard_cls(project)


class ProjectDashboard:
    def __init__(self, project):
        self.project = project

    def get_project_components(self):
        return [component for component in components.get_project_components()
                if component.is_effective(self.project)]

    def get_module_components(self):
        return components.get_module_components()

    def get_project_progress(self):
        num_valid = 0
        num_required = 0

        for component in self.get_project_components():
            if component.is_effective(self.project):
                nums = component.get_progress(self.project)
                num_valid = num_valid + nums[0]
                num_required = num_required + nums[1]

        return num_valid, num_required

    def get_module_progress(self, module):
        num_valid = 0
        num_required = 0

        for component in self.get_module_components():
            if component.is_effective(module):
                nums = component.get_progress(module)
                num_valid = num_valid + nums[0]
                num_required = num_required + nums[1]

        return num_valid, num_required

    def get_progress(self):
        num_valid = 0
        num_required = 0

        nums = self.get_project_progress()
        num_valid = num_valid + nums[0]
        num_required = num_required + nums[1]

        for module in self.project.modules.filter(is_draft=False):
            nums = self.get_module_progress(module)
            num_valid = num_valid + nums[0]
            num_required = num_required + nums[1]

        return num_valid, num_required

    def get_menu(self, current_module=None, current_component=None):
        project_menu = self.get_project_menu(current_component)

        menu_modules = []
        for module in self.project.modules:
            menu_module = self.get_module_menu(module, current_module,
                                               current_component)
            num_valid, num_required = self.get_module_progress(module)
            is_complete = (num_valid == num_required)

            if menu_module:
                menu_modules.append({
                    'module': module,
                    'menu': menu_module,
                    'is_complete': is_complete
                })

        return {'project': project_menu, 'modules': menu_modules}

    def get_project_menu(self, current_component):
        project_menu = []
        for component in self.get_project_components():
            if component.is_effective(self.project):
                is_active = (component == current_component)
                url = component.get_base_url(self.project)
                num_valid, num_required = component.get_progress(self.project)
                is_complete = (num_valid == num_required)

                project_menu.append({
                    'label': component.label,
                    'is_active': is_active,
                    'url': url,
                    'is_complete': is_complete,
                })
        return project_menu or None

    def get_module_menu(self, module, current_module, current_component):
        module_menu = []
        for component in self.get_module_components():
            if component.is_effective(module):
                is_active = (component == current_component and
                             module.pk == current_module.pk)
                url = component.get_base_url(module)
                num_valid, num_required = component.get_progress(module)
                is_complete = (num_valid == num_required)

                module_menu.append({
                    'label': component.label,
                    'is_active': is_active,
                    'url': url,
                    'is_complete': is_complete,
                })
        return module_menu or None
