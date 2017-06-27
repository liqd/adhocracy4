from django.shortcuts import get_object_or_404
from django.views import generic

from adhocracy4.projects import views as project_views

from . import models


class ExternalProjectRedirectView(project_views.ProjectContextDispatcher,
                                  generic.RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        extproject = get_object_or_404(models.ExternalProject,
                                       module=self.project.active_module)
        return extproject.url
