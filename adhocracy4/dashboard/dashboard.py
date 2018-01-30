from django.utils.translation import ugettext_lazy as _

from . import ModuleFormComponent
from . import ModuleFormSetComponent
from . import ProjectFormComponent
from . import components
from . import forms


class ProjectBasicComponent(ProjectFormComponent):
    identifier = 'basic'
    weight = 10
    label = _('Basic settings')

    form_title = _('Edit basic settings')
    form_class = forms.ProjectBasicForm
    form_template_name = 'a4dashboard/includes/project_basic_form.html'


class ProjectInformationComponent(ProjectFormComponent):
    identifier = 'information'
    weight = 11
    label = _('Information')

    form_title = _('Edit project information')
    form_class = forms.ProjectInformationForm
    form_template_name = 'a4dashboard/includes/project_information_form.html'


class ProjectResultComponent(ProjectFormComponent):
    identifier = 'result'
    weight = 12
    label = _('Result')

    form_title = _('Edit project result')
    form_class = forms.ProjectResultForm
    form_template_name = 'a4dashboard/includes/project_result_form.html'


class ModuleBasicComponent(ModuleFormComponent):
    identifier = 'module_basic'
    weight = 10
    label = _('Basic information')

    form_title = _('Edit basic module information')
    form_class = forms.ModuleBasicForm
    form_template_name = 'a4dashboard/includes/module_basic_form.html'


class ModulePhasesComponent(ModuleFormSetComponent):
    identifier = 'phases'
    weight = 11
    label = _('Phases')

    form_title = _('Edit phases information')
    form_class = forms.PhaseFormSet
    form_template_name = 'a4dashboard/includes/module_phases_form.html'


class ModuleAreaSettingsComponent(ModuleFormComponent):
    identifier = 'area_settings'
    weight = 12

    label = _('Areasettings')
    form_title = _('Edit areasettings')
    form_class = forms.AreaSettingsForm
    form_template_name = 'a4dashboard/includes/module_areasettings_form.html'

    def is_effective(self, module):
        module_settings = module.settings_instance
        return module_settings and hasattr(module_settings, 'polygon')

    def get_progress(self, module):
        module_settings = module.settings_instance
        if module_settings:
            return super().get_progress(module_settings)
        return 0, 0


components.register_module(ModuleAreaSettingsComponent())
components.register_module(ModuleBasicComponent())
components.register_module(ModulePhasesComponent())
components.register_project(ProjectBasicComponent())
components.register_project(ProjectResultComponent())
components.register_project(ProjectInformationComponent())
