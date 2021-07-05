from django.urls import reverse

from meinberlin.apps.exports.views import DashboardExportView


class PollDashboardExportView(DashboardExportView):
    template_name = 'meinberlin_exports/export_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_export'] = reverse(
            'a4dashboard:poll-comment-export',
            kwargs={'module_slug': self.module.slug})
        context['poll_export'] = reverse(
            'a4dashboard:poll-export',
            kwargs={'module_slug': self.module.slug})
        return context
