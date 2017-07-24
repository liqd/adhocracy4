from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views import generic

from adhocracy4.rules import mixins as rules_mixins
from adhocracy4.projects.models import Project

from . import models
from . import mixins


class ModuleDetailView(rules_mixins.PermissionRequiredMixin,
                       mixins.PhaseDispatchMixin,
                       generic.DetailView):
    model = models.Module
    permission_required = 'a4projects.view_project'
    slug_url_kwarg = 'module_slug'

    def get_permission_object(self):
        return self.get_object().project


class ModuleRedirectView(rules_mixins.PermissionRequiredMixin,
                         generic.RedirectView):
    permission_required = 'a4projects.view_project'
    permanent = False

    def dispatch(self, request, *args, **kwargs):
        project_slug = kwargs.get('slug')
        self.project = get_object_or_404(Project, slug=project_slug)
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse(
            'module-detail',
            kwargs={'module_slug': self.project.last_active_module.slug})

    def get_permission_object(self):
        return self.project
