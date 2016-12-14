from django.shortcuts import redirect
from django.views import generic
from rules.contrib import views as rules_views

from . import mixins, models


class ProjectDetailView(rules_views.PermissionRequiredMixin,
                        mixins.PhaseDispatchMixin,
                        generic.DetailView):

    model = models.Project
    permission_required = 'a4projects.view_project'

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated()

    def handle_no_permission(self):
        """
        Check if user clould join
        """
        membership_impossible = (
            not self.request.user.is_authenticated()
            or self.project.is_draft
            or self.project.has_member(self.request.user)
        )

        if membership_impossible:
            return super().handle_no_permission()
        else:
            return self._redirect_membership_request()

    def _redirect_membership_request(self):
        return redirect('memberships-request',
                        project_slug=self.project.slug)

    @property
    def project(self):
        """
        Emulate ProjectMixin interface for template sharing.
        """
        return self.get_object()
