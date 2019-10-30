from django.views import generic
from rules.contrib import views as rules_views

from . import mixins
from . import models


class ProjectDetailView(rules_views.PermissionRequiredMixin,
                        mixins.PhaseDispatchMixin,
                        generic.DetailView):

    model = models.Project
    permission_required = 'a4projects.view_project'

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated
