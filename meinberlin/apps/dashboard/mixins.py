from django.shortcuts import get_object_or_404
from django.utils import functional
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
