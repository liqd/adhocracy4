from django.http.response import HttpResponseRedirect
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
        if module.is_active_in_project:
            redirect_url = module.project.get_absolute_url()
            return HttpResponseRedirect(redirect_url)
        return super().dispatch(request, *args, **kwargs)

    @property
    def project(self):
        return self.get_object().project

    def get_permission_object(self):
        return self.project
