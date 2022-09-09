from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components

from . import exports
from . import views


class ExportBudgetingComponent(DashboardComponent):
    identifier = 'budgeting_export'
    weight = 50
    label = _('Export Excel')

    def is_effective(self, module):
        return (module.blueprint_type in ['PB', 'PB2', 'PB3'] and
                not module.project.is_draft and not module.is_draft)

    def get_progress(self, module):
        return 0, 0

    def get_base_url(self, module):
        return reverse('a4dashboard:budgeting-export-module', kwargs={
            'module_slug': module.slug,
        })

    def get_urls(self):
        return [
            (r'^modules/(?P<module_slug>[-\w_]+)/export/budgeting/$',
             views.ProposalDashboardExportView.as_view(),
             'budgeting-export-module'),
            (r'^modules/(?P<module_slug>[-\w_]+)/export/budgeting/ideas/$',
             exports.ProposalExportView.as_view(),
             'budgeting-export'),
            (r'^modules/(?P<module_slug>[-\w_]+)/export/budgeting/comments/$',
             exports.ProposalCommentExportView.as_view(),
             'budgeting-comment-export'),
        ]


components.register_module(ExportBudgetingComponent())
