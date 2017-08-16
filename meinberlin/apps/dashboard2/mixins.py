from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

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
        return reverse(
            'dashboard:project-list',
            kwargs={'organisation_slug': self.organisation.slug})


class BlueprintMixin:
    @property
    def blueprint(self):
        return dict(blueprints)[self.blueprint_key]

    @property
    def blueprint_key(self):
        return self.kwargs['blueprint_slug']


class DashboardMenuMixin:

    def get_menu(self):
        current_component = self.get_component()
        project = self.get_project()
        current_module = self.get_module()

        # FIXME: the menu items are in no specific order
        project_menu = self.get_project_menu(project, current_component)

        menu_modules = []
        for module in project.modules:
            menu_module = self.get_module_menu(module,
                                               current_component,
                                               current_module)
            if menu_module:
                menu_modules.append({
                    'module': module,
                    'menu': menu_module,
                })

        return {'project': project_menu, 'modules': menu_modules}

    @classmethod
    def get_project_menu(cls, project, current_component):
        project_menu = []
        for component in content.get_project_components():
            menu_item = component.get_menu_label(project)
            if menu_item:
                is_active = (component == current_component)
                url = reverse('a4dashboard:project-edit-component', kwargs={
                    'project_slug': project.slug,
                    'component_identifier': component.identifier
                })

                project_menu.append({
                    'label': menu_item,
                    'is_active': is_active,
                    'url': url,
                })
        return project_menu or None

    @classmethod
    def get_module_menu(cls, module, current_component, current_module):
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

                module_menu.append({
                    'label': menu_item,
                    'is_active': is_active,
                    'url': url,
                })
        return module_menu or None
