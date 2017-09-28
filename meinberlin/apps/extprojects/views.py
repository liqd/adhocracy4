from django.shortcuts import get_object_or_404
from django.views import generic

from meinberlin.apps.contrib.views import ProjectContextMixin
from meinberlin.apps.dashboard2.components.forms.views import \
    ProjectComponentFormView
from meinberlin.apps.dashboard2.views import ProjectCreateView

from . import forms
from . import models


class ExternalProjectRedirectView(ProjectContextMixin,
                                  generic.RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        extproject = get_object_or_404(models.ExternalProject,
                                       module=self.module)
        return extproject.url


class ExternalProjectCreateView(ProjectCreateView):

    model = models.ExternalProject
    slug_url_kwarg = 'project_slug'
    blueprint_key = 'external-project'
    form_class = forms.ExternalProjectCreateForm
    template_name = 'meinberlin_extprojects/external_project_create_form.html'


class ExternalProjectUpdateView(ProjectComponentFormView):

    model = models.ExternalProject
    module = None

    @property
    def project(self):
        project = super().project
        return project.externalproject

    def get_object(self, queryset=None):
        return self.project
