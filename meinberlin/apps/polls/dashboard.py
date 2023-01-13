from adhocracy4.dashboard import components
from adhocracy4.polls import dashboard as a4_poll_dashboard
from adhocracy4.polls import views as a4_poll_views

from . import exports


class ExportPollComponent(a4_poll_dashboard.ExportPollComponent):
    def get_urls(self):
        return [
            (
                r"^modules/(?P<module_slug>[-\w_]+)/poll/export/$",
                a4_poll_views.PollDashboardExportView.as_view(),
                "poll-export-module",
            ),
            (
                r"^modules/(?P<module_slug>[-\w_]+)/poll/export/comments/$",
                exports.PollCommentExportView.as_view(),
                "poll-comment-export",
            ),
            (
                r"^modules/(?P<module_slug>[-\w_]+)/poll/export/poll/$",
                exports.PollExportView.as_view(),
                "poll-export",
            ),
        ]


components.replace_module(ExportPollComponent())
