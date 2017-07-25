from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views import generic

from adhocracy4.rules import mixins as rules_mixins

from . import models


class ModuleDetailView(rules_mixins.PermissionRequiredMixin,
                       generic.DetailView):
    model = models.Module
    permission_required = 'a4projects.view_project'
    slug_url_kwarg = 'module_slug'

    def dispatch(self, request, *args, **kwargs):
        module = self.get_object()
        if module.is_active:
            return ModuleRedirectView.as_view()(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    @property
    def project(self):
        return self.get_object().project

    def get_permission_object(self):
        return self.project


class ModuleRedirectView(rules_mixins.PermissionRequiredMixin,
                         generic.RedirectView):
    permission_required = 'a4projects.view_project'
    permanent = False

    def dispatch(self, request, *args, **kwargs):
        module_slug = kwargs.get('module_slug')
        self.module = get_object_or_404(models.Module, slug=module_slug)
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse(
            'project-detail', kwargs={'slug': self.module.project.slug})

    def get_permission_object(self):
        return self.module.project
