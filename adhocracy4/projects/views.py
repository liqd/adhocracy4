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
        user = self.request.user
        is_member = user.is_authenticated() and self.project.has_member(user)

        if not is_member:
            return self.handle_no_membership()
        else:
            return super().handle_no_permission()

    def handle_no_membership(self):
        """
        Handle that an authenticated user is not member of project.

        Override this function to configure the behaviour if a user has no
        permissions to view the project and is not member of the project.
        """
        return super().handle_no_permission()


    @property
    def project(self):
        """
        Emulate ProjectMixin interface for template sharing.
        """
        return self.get_object()
