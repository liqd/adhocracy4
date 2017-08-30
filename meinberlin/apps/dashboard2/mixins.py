from copy import deepcopy
from datetime import datetime

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import base

from adhocracy4.modules import models as module_models
from adhocracy4.projects import models as project_models
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.contrib.views import ProjectContextDispatcher
from meinberlin.apps.organisations import models as org_models

from . import get_project_dashboard


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
        from .blueprints import blueprints
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

        dashboard = get_project_dashboard(project)

        context['dashboard_menu'] = dashboard.get_menu(self.module,
                                                       self.component)

        num_valid, num_required = dashboard.get_progress()
        context['project_progress'] = {
            'valid': num_valid,
            'required': num_required
        }

        return context


class DashboardProjectDuplicateMixin:
    def post(self, request, *args, **kwargs):
        if 'duplicate' in request.POST:
            pk = int(request.POST['project_pk'])
            project = get_object_or_404(project_models.Project, pk=pk)
            can_add = request.user.has_perm('a4projects.add_project',
                                            project)

            if not can_add:
                raise PermissionDenied

            project_clone = deepcopy(project)
            project_clone.pk = None
            if project_clone.tile_image:
                project_clone.tile_image.save(project.tile_image.name,
                                              project.tile_image, False)
            if project_clone.image:
                project_clone.image.save(project.image.name,
                                         project.image, False)
            project_clone.created = datetime.now()
            project_clone.is_draft = True
            project_clone.save()

            for module in project.module_set.all():
                module_clone = deepcopy(module)
                module_clone.project = project_clone
                module_clone.pk = None
                module_clone.name = \
                    '{}_{}'.format(module.name, project_clone.pk)
                module_clone.save()

                for phase in module.phase_set.all():
                    phase_clone = deepcopy(phase)
                    phase_clone.module = module_clone
                    phase_clone.pk = None
                    phase_clone.save()

                settings_instance = module.settings_instance
                if settings_instance:
                    settings_instance_clone = deepcopy(settings_instance)
                    settings_instance_clone.pk = None
                    settings_instance_clone.module = module_clone
                    settings_instance_clone.save()

            messages.success(request,
                             _('Project successfully duplicated.'))
            return redirect('a4dashboard:project-edit',
                            project_slug=project_clone.slug)
        else:
            return super().post(request, *args, **kwargs)
