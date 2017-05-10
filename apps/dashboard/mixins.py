from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils import functional
from django.utils.translation import ugettext as _
from django.views import generic
from rules.compat import access_mixins as mixins

from adhocracy4.projects import models as project_models
from adhocracy4.rules import mixins as rules_mixins

from apps.organisations import models as org_models
from apps.users.models import User


class DashboardBaseMixin(mixins.LoginRequiredMixin,
                         generic.base.ContextMixin):

    @functional.cached_property
    def organisation(self):
        if 'organisation_slug' in self.kwargs:
            slug = self.kwargs['organisation_slug']
            return get_object_or_404(org_models.Organisation, slug=slug)
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


class DashboardProjectPublishMixin:
    def post(self, request, *args, **kwargs):
        if 'submit_action' in request.POST:
            pk = int(request.POST['project_pk'])
            project = get_object_or_404(project_models.Project, pk=pk)
            can_edit = request.user.has_perm('a4projects.edit_project',
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


class DashboardModRemovalMixin:
    def post(self, request, *args, **kwargs):
        if 'submit_action' in request.POST:
            pk = int(request.POST['moderator_pk'])
            user = get_object_or_404(User, pk=pk)
            project = self.get_object()
            can_edit = request.user.has_perm(
                'a4projects.add_project',
                project
            )
            if not can_edit:
                raise PermissionDenied

            if request.POST['submit_action'] == 'remove_moderator':
                project.moderators.remove(user)
                messages.success(request, _('Moderator successfully removed.'))

            return redirect('dashboard-project-moderators',
                            slug=project.slug)
        else:
            return super().post(request, *args, **kwargs)
