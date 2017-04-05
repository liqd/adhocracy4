from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils import functional
from django.utils.translation import ugettext as _
from django.views import generic
from rules.compat import access_mixins as mixins

from adhocracy4.projects.models import Project
from apps.organisations.models import Organisation


class DashboardBaseMixin(mixins.LoginRequiredMixin,
                         generic.base.ContextMixin):

    @functional.cached_property
    def organisation(self):
        if 'organisation_slug' in self.kwargs:
            slug = self.kwargs['organisation_slug']
            return get_object_or_404(Organisation, slug=slug)
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


class DashboardProjectPublishMixin:
    def post(self, request, *args, **kwargs):
        pk = int(request.POST['project_pk'])
        project = get_object_or_404(Project, pk=pk)
        can_edit = request.user.has_perm('a4projects.edit_project', project)

        if not can_edit:
            raise PermissionDenied

        if 'publish' in request.POST:
            project.is_draft = False
            messages.success(request, _('Project successfully published.'))
        elif 'unpublish' in request.POST:
            project.is_draft = True
            messages.success(request, _('Project successfully unpublished.'))
        project.save()

        return redirect('dashboard-project-list',
                        organisation_slug=self.organisation.slug)
