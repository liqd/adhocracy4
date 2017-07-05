from django.shortcuts import get_object_or_404
from django.views import generic

from apps.contrib.views import ProjectContextDispatcher

from . import models


class ExternalProjectRedirectView(ProjectContextDispatcher,
                                  generic.RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        extproject = get_object_or_404(models.ExternalProject,
                                       module=self.project.last_active_module)
        return extproject.url
