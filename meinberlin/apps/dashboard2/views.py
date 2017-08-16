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
                                 generic.View):

    def dispatch(self, request, *args, **kwargs):
        project = self.get_project()
        component = self.get_component()
        menu = self.get_project_menu(project)

        kwargs['project'] = project
        kwargs['menu'] = menu

        return component.get_view()(request, *args, **kwargs)

    def get_component(self):
        if 'component_identifier' not in self.kwargs:
            raise Http404('Component not found')
        if self.kwargs['component_identifier'] not in content:
            raise Http404('Component not found')
        return content[self.kwargs['component_identifier']]

    def get_project(self):
        if 'project_slug' not in self.kwargs:
            raise Http404('Project not found')

        return get_object_or_404(project_models.Project,
                                 slug=self.kwargs['project_slug'])

    def get_project_menu(self, project):
        project_menu = []
        for component in content.get_project_components():
            menu_item = component.get_menu_item(project)
            if menu_item:
                is_active = (component == self.get_component())
                url = reverse('a4dashboard:project-edit-component', kwargs={
                    'project_slug': project.slug,
                    'component_identifier': component.identifier
                })

                project_menu.append({
                    'label': menu_item,
                    'is_active': is_active,
                    'url': url,
                })

        menu_modules = []
        for module in project.modules:
            menu_module = self.get_module_menu(module)
            if menu_module:
                menu_modules.append({
                    'module': module,
                    'menu': menu_modules,
                })

        return {'project': project_menu, 'modules': menu_modules}

    def get_module_menu(self, module):
        module_menu = []
        for component in content.get_module_components():
            menu_item = component.get_menu_item(module)
            if menu_item:
                # is_active = (component == self.get_component())
                is_active = False
                url = reverse('a4dashboard:project-edit-component', kwargs={
                    'project_slug': module.project.slug,
                    # 'module_slug':
                    'component_identifier': component.identifier
                })

                module_menu.append({
                    'label': menu_item,
                    'is_active': is_active,
                    'url': url,
                })
        return module_menu or None

