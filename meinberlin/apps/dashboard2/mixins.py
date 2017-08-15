from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from adhocracy4.projects import models as project_models
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.organisations import models as org_models

from .blueprints import blueprints


class DashboardBaseMixin(rules_mixins.PermissionRequiredMixin):

    @property
    def organisation(self):
        if 'organisation_slug' in self.kwargs:
            slug = self.kwargs['organisation_slug']
            return get_object_or_404(org_models.Organisation, slug=slug)

        # if hasattr(self, 'project'):
        #     return self.project.organisation

        if 'project_slug' in self.kwargs:
            slug = self.kwargs['project_slug']
            project = get_object_or_404(project_models.Project, slug=slug)
            return project.organisation

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
