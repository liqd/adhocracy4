from copy import deepcopy

from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import NoReverseMatch
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import base
from django.views.generic import edit

from adhocracy4.projects import models as project_models
from adhocracy4.rules import mixins as rules_mixins

from . import components
from . import get_project_dashboard
from . import signals

Organisation = apps.get_model(settings.A4_ORGANISATIONS_MODEL)


class DashboardBaseMixin(rules_mixins.PermissionRequiredMixin):
    organisation_lookup_field = 'slug'
    organisation_url_kwarg = 'organisation_slug'

    @property
    def organisation(self):
        if self.organisation_url_kwarg \
                and self.organisation_url_kwarg in self.kwargs:
            lookup = {
                self.organisation_lookup_field:
                    self.kwargs[self.organisation_url_kwarg]
            }
            return get_object_or_404(Organisation, **lookup)

        return self.project.organisation

    @property
    def other_organisations_of_user(self):
        user = self.request.user
        if self.organisation:
            initiator_orgs = user.organisation_set.all()
            if hasattr(Organisation, 'groups') and user.groups.all():
                user_groups = user.groups.all().values_list('id', flat=True)
                group_orgs = Organisation.objects\
                    .filter(groups__in=user_groups)
                orgs = initiator_orgs | group_orgs
                return orgs.distinct().exclude(pk=self.organisation.pk)
            return initiator_orgs.exclude(pk=self.organisation.pk)
        else:
            return None

    def get_permission_object(self):
        raise NotImplementedError('Set permission object.')

    def get_success_url(self):
        return self.request.path


class BlueprintMixin:
    @property
    def blueprint(self):
        from .blueprints import get_blueprints
        return dict(get_blueprints())[self.blueprint_key]

    @property
    def blueprint_key(self):
        return self.kwargs['blueprint_slug']


class DashboardComponentMixin(base.ContextMixin):
    """Set the menu_item and add dashboard information to the context data.

    Assumes self.project, self.module and self.component are set.
    """

    menu_item = 'project'
    component = None

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
        project_num_valid, project_num_required = \
            dashboard.get_project_progress()
        project_is_complete = (project_num_valid == project_num_required)
        context['project_progress'] = {
            'valid': num_valid,
            'required': num_required,
            'project_is_complete': project_is_complete
        }

        return context


class DashboardComponentFormSignalMixin(edit.FormMixin):
    def form_valid(self, form):
        response = super().form_valid(form)

        component = self.component
        if component.identifier in components.projects:
            signals.project_component_updated.send(sender=component.__class__,
                                                   project=self.project,
                                                   component=component,
                                                   user=self.request.user)
        else:
            signals.module_component_updated.send(sender=component.__class__,
                                                  module=self.module,
                                                  component=component,
                                                  user=self.request.user)
        return response


class DashboardComponentDeleteSignalMixin(edit.DeletionMixin):
    def delete(self, request, *args, **kwargs):
        # Project and module have to be stored before delete is called as
        # they may rely on the still existing db object.
        project = self.project
        module = self.module

        response = super().delete(request, *args, **kwargs)

        component = self.component
        if component.identifier in components.projects:
            signals.project_component_updated.send(sender=component.__class__,
                                                   project=project,
                                                   component=component,
                                                   user=self.request.user)
        else:
            signals.module_component_updated.send(sender=component.__class__,
                                                  module=module,
                                                  component=component,
                                                  user=self.request.user)
        return response


class DashboardProjectDuplicateMixin:
    def post(self, request, *args, **kwargs):
        if 'duplicate' in request.POST:
            pk = int(request.POST['project_pk'])
            project = get_object_or_404(project_models.Project, pk=pk)
            can_add = request.user.has_perm('a4projects.add_project',
                                            project)

            if not can_add:
                raise PermissionDenied()

            project_clone = deepcopy(project)
            project_clone.pk = None
            if project_clone.tile_image:
                project_clone.tile_image.save(project.tile_image.name,
                                              project.tile_image, False)
            if project_clone.image:
                project_clone.image.save(project.image.name,
                                         project.image, False)
            project_clone.created = timezone.now()
            project_clone.is_draft = True
            project_clone.is_archived = False
            project_clone.save()
            signals.project_created.send(sender=None,
                                         project=project_clone,
                                         user=self.request.user)

            for moderator in project.moderators.all():
                project_clone.moderators.add(moderator)

            for module in project.module_set.all():
                module_clone = deepcopy(module)
                module_clone.project = project_clone
                module_clone.pk = None
                module_clone.save()
                signals.module_created.send(sender=None,
                                            module=module_clone,
                                            user=self.request.user)

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

            try:
                org_slug = project_clone.organisation.slug
                return redirect('a4dashboard:project-edit',
                                organisation_slug=org_slug,
                                project_slug=project_clone.slug)
            except NoReverseMatch:
                return redirect('a4dashboard:project-edit',
                                project_slug=project_clone.slug)
        else:
            return super().post(request, *args, **kwargs)
