from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import base

from adhocracy4.modules import models as module_models
from adhocracy4.projects import models as project_models
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.organisations import models as org_models

from .blueprints import blueprints
from .contents import content


class DashboardBaseMixin(rules_mixins.PermissionRequiredMixin):

    @property
    def organisation(self):
        if 'organisation_slug' in self.kwargs:
            slug = self.kwargs['organisation_slug']
            return get_object_or_404(org_models.Organisation, slug=slug)

        if 'project_slug' in self.kwargs:
            slug = self.kwargs['project_slug']
            project = get_object_or_404(project_models.Project, slug=slug)
            return project.organisation

        if 'module_slug' in self.kwargs:
            slug = self.kwargs['module_slug']
            module = get_object_or_404(module_models.Module, slug=slug)
            return module.project.organisation

        raise ObjectDoesNotExist()

    def get_permission_object(self):
        return self.organisation

    def get_success_url(self):
        return self.request.path


class BlueprintMixin:
    @property
    def blueprint(self):
        return dict(blueprints)[self.blueprint_key]

    @property
    def blueprint_key(self):
        return self.kwargs['blueprint_slug']


class DashboardComponentMixin(base.ContextMixin,
                              base.View):

    def dispatch(self, request, project, module, *args, **kwargs):
        self.module = module
        self.project = project
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        context['module'] = self.module
        return context


class DashboardContextMixin(base.ContextMixin):
    """Add dashboard information to the context data.

    Assumes self.project, self.module and self.component are set.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dashboard_menu'] = self.get_dashboard_menu()
        context['project_progress'] = self.get_project_progress()
        return context

    def get_project_progress(self):
        num_valid = 0
        num_required = 0

        for component in content.get_project_components():
            nums = component.get_progress(self.project)
            num_valid = num_valid + nums[0]
            num_required = num_required + nums[1]

        for module in self.project.modules:
            for component in content.get_module_components():
                nums = component.get_progress(module)
                num_valid = num_valid + nums[0]
                num_required = num_required + nums[1]

        return {
            'valid': num_valid,
            'required': num_required
        }

    def get_dashboard_menu(self):
        # FIXME: the menu items are in no specific order
        project_menu = self.get_project_menu(self.project, self.component)

        menu_modules = []
        for module in self.project.modules:
            menu_module = self.get_module_menu(module,
                                               self.component,
                                               self.module)
            if menu_module:
                menu_modules.append({
                    'module': module,
                    'menu': menu_module,
                })

        return {'project': project_menu, 'modules': menu_modules}

    @staticmethod
    def get_project_menu(project, current_component):
        project_menu = []
        for component in content.get_project_components():
            menu_item = component.get_menu_label(project)
            if menu_item:
                is_active = (component == current_component)
                url = reverse('a4dashboard:project-edit-component', kwargs={
                    'project_slug': project.slug,
                    'component_identifier': component.identifier
                })
                num_valid, num_required = component.get_progress(project)
                is_complete = (num_valid == num_required)

                project_menu.append({
                    'label': menu_item,
                    'is_active': is_active,
                    'url': url,
                    'is_complete': is_complete,
                })
        return project_menu or None

    @staticmethod
    def get_module_menu(module, current_component, current_module):
        module_menu = []
        for component in content.get_module_components():
            menu_item = component.get_menu_label(module)
            if menu_item:
                is_active = (component == current_component and
                             module.pk == current_module.pk)
                url = reverse('a4dashboard:module-edit-component', kwargs={
                    'module_slug': module.slug,
                    'component_identifier': component.identifier
                })
                num_valid, num_required = component.get_progress(module)
                is_complete = (num_valid == num_required)

                module_menu.append({
                    'label': menu_item,
                    'is_active': is_active,
                    'url': url,
                    'is_complete': is_complete,
                })
        return module_menu or None
