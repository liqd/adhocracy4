from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import functional
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.organisations.models import Organisation

from . import blueprints
from . import forms
from . import mixins
from .contents import content

User = get_user_model()


def get_object_or_none(*args, **kwargs):
    try:
        return get_object_or_404(*args, **kwargs)
    except Http404:
        return None


class ProjectListView(rules_mixins.PermissionRequiredMixin,
                      generic.ListView):
    model = project_models.Project
    paginate_by = 12
    template_name = 'meinberlin_dashboard2/project_list.html'
    permission_required = 'a4projects.add_project'

    @functional.cached_property
    def organisation(self):
        if 'organisation_slug' in self.kwargs:
            slug = self.kwargs['organisation_slug']
            return get_object_or_404(Organisation, slug=slug)

    def get_permission_object(self):
        return self.organisation

    def get_queryset(self):
        return super().get_queryset().filter(
            organisation=self.organisation
        )


class BlueprintListView(mixins.DashboardBaseMixin,
                        generic.TemplateView):
    blueprints = blueprints.blueprints
    template_name = 'meinberlin_dashboard2/blueprint_list.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'


class ProjectCreateView(mixins.DashboardBaseMixin,
                        mixins.BlueprintMixin,
                        generic.CreateView,
                        SuccessMessageMixin):
    model = project_models.Project
    form_class = forms.ProjectCreateForm
    template_name = 'meinberlin_dashboard2/project_create_form.html'
    permission_required = 'a4projects.add_project'
    success_message = _('Project succesfully created.')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['type'] = self.blueprint_key
        kwargs['organisation'] = self.organisation
        kwargs['creator'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('a4dashboard:project-edit',
                       kwargs={'project_slug': self.object.slug})

    def form_valid(self, form):
        response = super().form_valid(form)

        # FIXME: maybe replace by dashboard signals
        self._create_modules_and_phases(self.object)

        return response

    def _create_modules_and_phases(self, project):
        module = module_models.Module(
            name=project.slug + '_module',
            weight=1,
            project=project,
        )
        module.save()
        self._create_phases(module, self.blueprint.content)

    def _create_phases(self, module, blueprint_phases):
        for phase_content in blueprint_phases:
            phase = phase_models.Phase(
                type=phase_content.identifier,
                name=phase_content.name,
                description=phase_content.description,
                weight=phase_content.weight,
                module=module,
            )
            phase.save()


class ProjectUpdateView(mixins.DashboardBaseMixin,
                        generic.UpdateView,
                        SuccessMessageMixin):
    model = project_models.Project
    slug_url_kwarg = 'project_slug'
    form_class = forms.ProjectUpdateForm
    template_name = 'meinberlin_dashboard2/project_update_form.html'
    permission_required = 'a4projects.add_project'
    success_message = _('Project successfully created.')


class ProjectComponentDispatcher(mixins.DashboardBaseMixin,
                                 mixins.DashboardMenuMixin,
                                 generic.View):

    def dispatch(self, request, *args, **kwargs):
        project = self.get_project()
        if not project:
            raise Http404('Project not found')

        component = self.get_component()
        if not component:
            raise Http404('Component not found')

        menu = self.get_menu()

        kwargs['module'] = None
        kwargs['project'] = project
        kwargs['menu'] = menu

        return component.get_view()(request, *args, **kwargs)

    def get_component(self):
        if 'component_identifier' not in self.kwargs:
            return None
        if self.kwargs['component_identifier'] not in content:
            return None
        return content[self.kwargs['component_identifier']]

    def get_project(self):
        if 'project_slug' not in self.kwargs:
            return None
        return get_object_or_none(project_models.Project,
                                  slug=self.kwargs['project_slug'])

    def get_module(self):
        return None


class ModuleComponentDispatcher(mixins.DashboardBaseMixin,
                                mixins.DashboardMenuMixin,
                                generic.View):

    def dispatch(self, request, *args, **kwargs):
        module = self.get_module()
        if not module:
            raise Http404('Module not found')

        component = self.get_component()
        if not component:
            raise Http404('Component not found')

        menu = self.get_menu()

        kwargs['module'] = module
        kwargs['project'] = module.project
        kwargs['menu'] = menu

        return component.get_view()(request, *args, **kwargs)

    def get_component(self):
        if 'component_identifier' not in self.kwargs:
            return None
        if self.kwargs['component_identifier'] not in content:
            return None
        return content[self.kwargs['component_identifier']]

    def get_module(self):
        if 'module_slug' not in self.kwargs:
            return None
        return get_object_or_none(module_models.Module,
                                  slug=self.kwargs['module_slug'])

    def get_project(self):
        return self.get_module().project


class ProjectBasicComponentView(mixins.DashboardBaseMixin,
                                generic.UpdateView,
                                SuccessMessageMixin):
    permission_required = 'a4projects.add_project'
    model = project_models.Project
    form_class = forms.ProjectBasicForm
    template_name = 'meinberlin_dashboard2/base_form_project.html'
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/project_basic_form.html'
    title = _('Edit basic settings')
    success_message = _('Project successfully updated.')

    def dispatch(self, request, project, menu, *args, **kwargs):
        self.project = project
        self.menu = menu
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dashboard_menu'] = self.menu
        context['project'] = self.project
        return context


class ProjectInformationComponentView(mixins.DashboardBaseMixin,
                                      generic.UpdateView,
                                      SuccessMessageMixin):
    permission_required = 'a4projects.add_project'
    model = project_models.Project
    form_class = forms.ProjectInformationForm
    template_name = 'meinberlin_dashboard2/base_form_project.html'
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/project_information_form.html'
    title = _('Edit project information')
    success_message = _('Project successfully updated.')

    def dispatch(self, request, project, menu, *args, **kwargs):
        self.project = project
        self.menu = menu
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dashboard_menu'] = self.menu
        context['project'] = self.project
        return context


class ModulePhasesComponentView(mixins.DashboardBaseMixin,
                                generic.UpdateView,
                                SuccessMessageMixin):
    permission_required = 'a4projects.add_project'
    model = project_models.Project
    form_class = forms.ModulePhasesForm
    template_name = 'meinberlin_dashboard2/base_form_module.html'
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/module_phases_form.html'
    title = _('Edit phases information')
    success_message = _('Project successfully updated.')

    def dispatch(self, request, project, module, menu, *args, **kwargs):
        self.module = module
        self.project = project
        self.menu = menu
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dashboard_menu'] = self.menu
        context['project'] = self.project
        context['module'] = self.module
        return context
