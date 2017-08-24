from copy import deepcopy

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.views.generic import base

from adhocracy4.modules import models as module_models
from adhocracy4.projects import models as project_models
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.contrib.views import ProjectContextDispatcher
from meinberlin.apps.organisations import models as org_models

from . import components
from .blueprints import blueprints


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

    @property
    def other_organisations_of_user(self):
        user = self.request.user
        if self.organisation:
            return user.organisation_set.exclude(pk=self.organisation.pk)
        else:
            return None

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


class DashboardComponentMixin(ProjectContextDispatcher):
    menu_item = 'project'
    component = None


class DashboardContextMixin(base.ContextMixin):
    """Add dashboard information to the context data.

    Assumes self.project, self.module and self.component are set.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Workaround Djangos update behavior:
        # All fields from the POST data will be set on the view.object model
        # instance, regardless of validation errors.
        # Thus it is not reliable to check on empty fields on the view.object
        # but it has to be ensured that the model reflects the database.
        project = deepcopy(self.project)
        if project:
            project.refresh_from_db()
        module = deepcopy(self.module)
        if module:
            module.refresh_from_db()

        context['dashboard_menu'] = self.get_dashboard_menu(project, module,
                                                            self.component)
        context['project_progress'] = self.get_project_progress(project)
        return context

    @staticmethod
    def get_project_progress(project):
        num_valid = 0
        num_required = 0

        for component in components.get_project_components():
            nums = component.get_progress(project)
            num_valid = num_valid + nums[0]
            num_required = num_required + nums[1]

        for module in project.modules:
            for component in components.get_module_components():
                nums = component.get_progress(module)
                num_valid = num_valid + nums[0]
                num_required = num_required + nums[1]

        return {
            'valid': num_valid,
            'required': num_required
        }

    @staticmethod
    def get_dashboard_menu(project, current_module, current_component):
        cls = DashboardContextMixin
        # FIXME: the menu items are in no specific order
        project_menu = cls.get_project_menu(project, current_component)

        menu_modules = []
        for module in project.modules:
            menu_module = cls.get_module_menu(module,
                                              current_component,
                                              current_module)
            if menu_module:
                menu_modules.append({
                    'module': module,
                    'menu': menu_module,
                })

        return {'project': project_menu, 'modules': menu_modules}

    @staticmethod
    def get_project_menu(project, current_component):
        project_menu = []
        for component in components.get_project_components():
            menu_item = component.get_menu_label(project)
            if menu_item:
                is_active = (component == current_component)
                url = component.get_base_url(project)
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
        for component in components.get_module_components():
            menu_item = component.get_menu_label(module)
            if menu_item:
                is_active = (component == current_component and
                             module.pk == current_module.pk)
                url = component.get_base_url(module)
                num_valid, num_required = component.get_progress(module)
                is_complete = (num_valid == num_required)

                module_menu.append({
                    'label': menu_item,
                    'is_active': is_active,
                    'url': url,
                    'is_complete': is_complete,
                })
        return module_menu or None
