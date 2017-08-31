from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from adhocracy4.categories.models import Categorizable

from . import DashboardComponent
from . import ModuleFormComponent
from . import ModuleFormSetComponent
from . import ProjectFormComponent
from . import components
from . import forms
from . import get_project_type
from . import views


class ProjectBasicComponent(ProjectFormComponent):
    identifier = 'basic'
    weight = 10
    label = _('Basic settings')

    form_title = _('Edit basic settings')
    form_class = forms.ProjectBasicForm
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/project_basic_form.html'


class ProjectInformationComponent(ProjectFormComponent):
    identifier = 'information'
    weight = 11
    label = _('Information')

    form_title = _('Edit project information')
    form_class = forms.ProjectInformationForm
    form_template_name = 'meinberlin_dashboard2' \
                         '/includes/project_information_form.html'


class ProjectResultComponent(ProjectFormComponent):
    identifier = 'result'
    weight = 12
    label = _('Result')

    form_title = _('Edit project result')
    form_class = forms.ProjectResultForm
    form_template_name = 'meinberlin_dashboard2' \
                         '/includes/project_result_form.html'


class ModuleBasicComponent(ModuleFormComponent):
    identifier = 'module_basic'
    weight = 10
    label = _('Basic information')

    form_title = _('Edit basic module information')
    form_class = forms.ModuleBasicForm
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/module_basic_form.html'


class ModulePhasesComponent(ModuleFormSetComponent):
    identifier = 'phases'
    weight = 11
    label = _('Phases')

    form_title = _('Edit phases information')
    form_class = forms.PhaseFormSet
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/module_phases_form.html'


class ModuleAreaSettingsComponent(ModuleFormComponent):
    identifier = 'area_settings'
    weight = 12

    label = _('Areasettings')
    form_title = _('Edit areasettings')
    form_class = forms.AreaSettingsForm
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/module_areasettings_form.html'

    def is_effective(self, module):
        module_settings = module.settings_instance
        return module_settings and hasattr(module_settings, 'polygon')

    def get_progress(self, module):
        module_settings = module.settings_instance
        if module_settings:
            return super().get_progress(module_settings)
        return 0, 0


class ModuleCategoriesComponent(ModuleFormSetComponent):
    identifier = 'categories'
    weight = 13
    label = _('Categories')

    form_title = _('Edit categories')
    form_class = forms.CategoryFormSet
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/module_categories_form.html'

    def is_effective(self, module):
        for phase in module.phases:
            for models in phase.content().features.values():
                for model in models:
                    if Categorizable.is_categorizable(model):
                        return True
        return False


class ParticipantsComponent(DashboardComponent):
    identifier = 'participants'
    weight = 30
    label = _('Participants')

    def is_effective(self, project):
        return project.is_private

    def get_base_url(self, project):
        return reverse('a4dashboard:dashboard-participants-edit', kwargs={
            'project_slug': project.slug
        })

    def get_urls(self):
        return [(
            r'^projects/(?P<project_slug>[-\w_]+)/participants/$',
            views.DashboardProjectParticipantsView.as_view(component=self),
            'dashboard-participants-edit'
        )]


class ModeratorsComponent(DashboardComponent):
    identifier = 'moderators'
    weight = 31
    label = _('Moderators')

    def is_effective(self, project):
        return True

    def get_base_url(self, project):
        return reverse('a4dashboard:dashboard-moderators-edit', kwargs={
            'project_slug': project.slug
        })

    def get_urls(self):
        return [(
            r'^projects/(?P<project_slug>[-\w_]+)/moderators/$',
            views.DashboardProjectModeratorsView.as_view(component=self),
            'dashboard-moderators-edit'
        )]


class ExternalProjectComponent(ProjectFormComponent):
    identifier = 'external'
    weight = 10
    label = _('External project settings')

    form_title = _('Edit external project settings')
    form_class = forms.ExternalProjectForm
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/external_project_form.html'

    def is_effective(self, project):
        project_type = get_project_type(project)
        return project_type == 'external'

    def get_base_url(self, project):
        return reverse('a4dashboard:dashboard-external-project-edit', kwargs={
            'project_slug': project.slug
        })

    def get_urls(self):
        return [(
            r'^projects/(?P<project_slug>[-\w_]+)/external/$',
            views.ExternalProjectUpdateView.as_view(
                component=self,
                title=self.form_title,
                form_class=self.form_class,
                form_template_name=self.form_template_name
            ),
            'dashboard-external-project-edit'
        )]

    def get_progress(self, project):
        project = project.externalproject

        num_valid, num_required = super().get_progress(project)
        phase_num_valid, phase_num_required = \
            self._get_progress_for_object(project.phase,
                                          ['start_date', 'end_date'])

        return num_valid + phase_num_valid, num_required + phase_num_required


class BplanProjectComponent(ProjectFormComponent):
    identifier = 'bplan'
    weight = 10
    label = _('Development plan settings')

    form_title = _('Edit development plan settings')
    form_class = forms.BplanProjectForm
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/bplan_project_form.html'

    def is_effective(self, project):
        project_type = get_project_type(project)
        return project_type == 'bplan'

    def get_base_url(self, project):
        return reverse('a4dashboard:dashboard-bplan-project-edit', kwargs={
            'project_slug': project.slug
        })

    def get_urls(self):
        return [(
            r'^projects/(?P<project_slug>[-\w_]+)/bplan/$',
            views.BplanProjectUpdateView.as_view(
                component=self,
                title=self.form_title,
                form_class=self.form_class,
                form_template_name=self.form_template_name
            ),
            'dashboard-bplan-project-edit'
        )]

    def get_progress(self, project):
        project = project.externalproject.bplan

        num_valid, num_required = super().get_progress(project)
        phase_num_valid, phase_num_required = \
            self._get_progress_for_object(project.phase,
                                          ['start_date', 'end_date'])

        return num_valid + phase_num_valid, num_required + phase_num_required


components.register_module(ModuleAreaSettingsComponent())
components.register_module(ModuleBasicComponent())
components.register_module(ModuleCategoriesComponent())
components.register_module(ModulePhasesComponent())
components.register_project(BplanProjectComponent())
components.register_project(ExternalProjectComponent())
components.register_project(ModeratorsComponent())
components.register_project(ParticipantsComponent())
components.register_project(ProjectBasicComponent())
components.register_project(ProjectInformationComponent())
