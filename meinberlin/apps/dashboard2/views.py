from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import functional
from django.views import generic

from adhocracy4.projects import models as project_models
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.organisations.models import Organisation

User = get_user_model()


class DashboardProjectListView(rules_mixins.PermissionRequiredMixin,
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
