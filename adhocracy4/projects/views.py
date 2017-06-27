from django.views import generic
from rules.contrib import views as rules_views

from . import mixins, models


class ProjectDetailView(rules_views.PermissionRequiredMixin,
                        mixins.PhaseDispatcher,
                        generic.DetailView):

    model = models.Project
    permission_required = 'a4projects.view_project'

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated()

    @property
    def project(self):
        """
        Emulate ProjectMixin interface for template sharing.
        """
        return self.get_object()
