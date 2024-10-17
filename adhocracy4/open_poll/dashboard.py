from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components

from . import exports
from . import models
from . import views


class OpenPollComponent(DashboardComponent):
    identifier = "open_polls"
    weight = 20
    label = _("Open Poll")

    def is_effective(self, module):
        module_app = module.phases[0].content().app
        return module_app == "a4open_poll"

    def get_progress(self, module):
        if models.Question.objects.filter(poll__module=module).exists():
            return 1, 1
        return 0, 1

    def get_base_url(self, module):
        return reverse(
            "a4dashboard:open-poll-dashboard", kwargs={"module_slug": module.slug}
        )

    def get_urls(self):
        return [
            (
                r"^modules/(?P<module_slug>[-\w_]+)/opent_poll/$",
                views.OpenPollDashboardView.as_view(component=self),
                "open-poll-dashboard",
            )
        ]


class ExportOpenPollComponent(DashboardComponent):
    identifier = "open-poll_export"
    weight = 50
    label = _("Export Excel")

    def is_effective(self, module):
        module_app = module.phases[0].content().app
        return (
            module_app == "a4open-polls"
            and not module.project.is_draft
            and not module.is_draft
        )

    def get_progress(self, module):
        return 0, 0

    def get_base_url(self, module):
        return reverse(
            "a4dashboard:poll-export-module",
            kwargs={
                "module_slug": module.slug,
            },
        )

    def get_urls(self):
        return [
            (
                r"^modules/(?P<module_slug>[-\w_]+)/poll/export/$",
                views.OpenPollDashboardExportView.as_view(),
                "open-poll-export-module",
            ),
            (
                r"^modules/(?P<module_slug>[-\w_]+)/poll/export/comments/$",
                exports.OpenPollCommentExportView.as_view(),
                "poll-comment-export",
            ),
            (
                r"^modules/(?P<module_slug>[-\w_]+)/poll/export/poll/$",
                exports.OpenPollExportView.as_view(),
                "open-poll-export",
            ),
        ]


components.register_module(OpenPollComponent())
components.register_module(ExportOpenPollComponent())
