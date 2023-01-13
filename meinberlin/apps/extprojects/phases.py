from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import generic

from adhocracy4 import phases
from adhocracy4.projects.mixins import ProjectMixin

from . import apps
from . import models


class ExternalProjectRedirectView(ProjectMixin, generic.RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        extproject = get_object_or_404(models.ExternalProject, module=self.module)
        return extproject.url


class ExternalPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = "external"
    view = ExternalProjectRedirectView

    name = _("External phase")
    description = _("External phase.")
    module_name = _("external project")

    features = {}


phases.content.register(ExternalPhase())
