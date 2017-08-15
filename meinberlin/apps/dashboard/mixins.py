from copy import deepcopy
from datetime import datetime

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils import functional
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.projects import models as project_models
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.organisations import models as org_models


class DashboardBaseMixin(rules_mixins.PermissionRequiredMixin,
                         generic.base.ContextMixin):

    @functional.cached_property
    def organisation(self):
        if 'organisation_slug' in self.kwargs:
            slug = self.kwargs['organisation_slug']
            return get_object_or_404(org_models.Organisation, slug=slug)
        if hasattr(self, 'project'):
            return self.project.organisation
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
            project = get_object_or_404(project_models.Project, slug=slug)
            return project.organisation
        else:
            return self.request.user.organisation_set.first()

    @functional.cached_property
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


class DashboardProjectBaseMixin(DashboardBaseMixin,
                                rules_mixins.PermissionRequiredMixin):
    permission_required = 'a4projects.add_project'
    menu_item = 'project'

    def get_success_url(self):
        return reverse(
            'dashboard-project-list',
            kwargs={'organisation_slug': self.organisation.slug, })


class DashboardProjectCreateMixin(DashboardProjectBaseMixin,
                                  SuccessMessageMixin,
                                  generic.CreateView):
    success_message = _('Project succesfully created.')

    def get_form_kwargs(self):
        kwargs = super(DashboardProjectCreateMixin, self).get_form_kwargs()
        kwargs['blueprint'] = self.blueprint
        kwargs['blueprint_key'] = self.blueprint_key
        kwargs['organisation'] = self.organisation
        kwargs['creator'] = self.request.user
        return kwargs


class DashboardProjectUpdateMixin(DashboardProjectBaseMixin,
                                  SuccessMessageMixin,
                                  generic.UpdateView):
    success_message = _('Project successfully updated.')

    def get_queryset(self):
        return super().get_queryset().filter(
            organisation=self.organisation
        )


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
            messages.success(request,
                             _('Project successfully duplicated.'))
            return redirect('dashboard-project-edit', slug=project_clone.slug)
        else:
            return super().post(request, *args, **kwargs)


class DashboardProjectPublishMixin:
    def post(self, request, *args, **kwargs):
        if 'submit_action' in request.POST:
            pk = int(request.POST['project_pk'])
            project = get_object_or_404(project_models.Project, pk=pk)
            can_edit = request.user.has_perm('a4projects.change_project',
                                             project)

            if not can_edit:
                raise PermissionDenied

            if request.POST['submit_action'] == 'publish':
                phases = project.phases

                # Assure that every phase has a start and an end date
                missing_date = False
                for phase in phases:
                    if not phase.start_date or not phase.end_date:
                        missing_date = True
                        break

                if missing_date:
                    messages.error(request,
                                   _('Project can not be published until'
                                     ' every Phase it contains has start and'
                                     ' end dates.'))
                else:
                    project.is_draft = False
                    messages.success(request,
                                     _('Project successfully published.'))
                    project.save()

            elif request.POST['submit_action'] == 'unpublish':
                project.is_draft = True
                messages.success(request,
                                 _('Project successfully unpublished.'))
                project.save()

        return redirect('dashboard-project-list',
                        organisation_slug=self.organisation.slug)
