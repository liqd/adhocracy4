from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils import functional
from django.views import generic
from rules.compat import access_mixins as mixins

from adhocracy4.contrib.views import PermissionRequiredMixin
from adhocracy4.projects import models as project_models

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


class DashboardProjectListView(DashboardBaseMixin,
                               PermissionRequiredMixin,
                               generic.ListView):
    model = project_models.Project
    template_name = 'meinberlin_dashboard/project_list.html'
    permission_required = 'meinberlin_organisations.initiate_project'
    menu_item = 'project'

    def get_queryset(self):
        return self.model.objects.filter(
            organisation=self.organisation
        )

    def get_permission_object(self):
        return self.organisation

    def get_success_url(self):
        return reverse('dashboard-project-list')
