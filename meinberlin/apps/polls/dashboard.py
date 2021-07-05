from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components

from . import exports
from . import views


class ExportPollComponent(DashboardComponent):
    identifier = 'poll_export'
    weight = 50
    label = _('Export Excel')

    def is_effective(self, module):
        module_app = module.phases[0].content().app
        return module_app == 'a4polls' and not module.project.is_draft

    def get_progress(self, module):
        return 0, 0

    def get_base_url(self, module):
        return reverse('a4dashboard:poll-export-module', kwargs={
            'module_slug': module.slug,
        })

    def get_urls(self):
        return [
            (r'^modules/(?P<module_slug>[-\w_]+)/poll/export/$',
             views.PollDashboardExportView.as_view(),
             'poll-export-module'),
            (r'^modules/(?P<module_slug>[-\w_]+)/poll/export/comments/$',
             exports.PollCommentExportView.as_view(),
             'poll-comment-export'),
            (r'^modules/(?P<module_slug>[-\w_]+)/poll/export/poll/$',
             exports.PollExportView.as_view(),
             'poll-export'),
        ]


components.register_module(ExportPollComponent())
