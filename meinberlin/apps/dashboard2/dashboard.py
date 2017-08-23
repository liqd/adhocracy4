from django.utils.translation import ugettext_lazy as _

from . import ModuleFormComponent
from . import ModuleFormSetComponent
from . import ProjectFormComponent
from . import content
from . import forms


class ProjectBasicComponent(ProjectFormComponent):
    identifier = 'basic'
    weight = 10

    menu_label = _('Basic settings')
    form_title = _('Edit basic settings')
    form_class = forms.ProjectBasicForm
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/project_basic_form.html'


class ProjectInformationComponent(ProjectFormComponent):
    identifier = 'information'
    weight = 11

    menu_label = _('Information')
    form_title = _('Edit project information')
    form_class = forms.ProjectInformationForm
    form_template_name = 'meinberlin_dashboard2' \
                         '/includes/project_information_form.html'


class ProjectResultComponent(ProjectFormComponent):
    identifier = 'result'
    weight = 12

    menu_label = _('Result')
    form_title = _('Edit project result')
    form_class = forms.ProjectResultForm
    form_template_name = 'meinberlin_dashboard2' \
                         '/includes/project_result_form.html'


class ModuleBasicComponent(ModuleFormComponent):
    identifier = 'module_basic'
    weight = 10

    menu_label = _('Basic information')
    form_title = _('Edit basic module information')
    form_class = forms.ModuleBasicForm
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/module_basic_form.html'


class ModulePhasesComponent(ModuleFormSetComponent):
    identifier = 'phases'
    weight = 11

    menu_label = _('Phases')
    form_title = _('Edit phases information')
    form_class = forms.PhaseFormSet
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/module_phases_form.html'


content.register_project(ProjectBasicComponent())
content.register_project(ProjectInformationComponent())
content.register_project(ProjectResultComponent())
content.register_module(ModuleBasicComponent())
content.register_module(ModulePhasesComponent())
