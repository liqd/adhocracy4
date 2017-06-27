from django.shortcuts import get_object_or_404
from django.views import generic

from adhocracy4.projects import mixins as project_mixins

from . import models


class ExternalProjectRedirectView(project_mixins.ProjectMixin,
                                  generic.RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        extproject = get_object_or_404(models.ExternalProject,
                                       module=self.project.active_module)
        return extproject.url
