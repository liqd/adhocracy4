from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components

from . import views


class AdminLogComponent(DashboardComponent):
    identifier = "adminlog"
    weight = 60
    label = _("Log")

    def is_effective(self, project):
        return True

    def get_progress(self, project):
        return 0, 0

    def get_base_url(self, project):
        return reverse(
            "a4dashboard:adminlog",
            kwargs={
                "project_slug": project.slug,
            },
        )

    def get_urls(self):
        return [
            (
                r"^projects/(?P<project_slug>[-\w_]+)/log/$",
                views.AdminLogProjectDashboardView.as_view(component=self),
                "adminlog",
            ),
        ]


components.register_project(AdminLogComponent())
