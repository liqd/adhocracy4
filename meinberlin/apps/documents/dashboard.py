from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components
from meinberlin.apps.documents.models import Chapter

from . import exports
from . import views


class DocumentComponent(DashboardComponent):
    identifier = 'document_settings'
    weight = 20
    label = _('Document')

    def is_effective(self, module):
        return module.blueprint_type == 'TR'

    def get_progress(self, module):
        if Chapter.objects.filter(module=module).exists():
            return 1, 1
        return 0, 1

    def get_base_url(self, module):
        return reverse('a4dashboard:dashboard-document-settings', kwargs={
            'module_slug': module.slug
        })

    def get_urls(self):
        return [(
            r'^modules/(?P<module_slug>[-\w_]+)/document/$',
            views.DocumentDashboardView.as_view(component=self),
            'dashboard-document-settings'
        )]


components.register_module(DocumentComponent())


class ExportDocumentComponent(DashboardComponent):
    identifier = 'document_export'
    weight = 50
    label = _('Export Excel')

    def is_effective(self, module):
        return (module.blueprint_type == 'TR' and
                not module.project.is_draft and not module.is_draft)

    def get_progress(self, module):
        return 0, 0

    def get_base_url(self, module):
        return reverse('a4dashboard:document-export-module', kwargs={
            'module_slug': module.slug,
        })

    def get_urls(self):
        return [
            (r'^modules/(?P<module_slug>[-\w_]+)/export/document/$',
             views.DocumentDashboardExportView.as_view(),
             'document-export-module'),
            (r'^modules/(?P<module_slug>[-\w_]+)/export/document/comments/$',
             exports.DocumentExportView.as_view(),
             'document-comment-export'),
        ]


components.register_module(ExportDocumentComponent())
