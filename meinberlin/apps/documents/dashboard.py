from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from meinberlin.apps.dashboard2 import DashboardComponent
from meinberlin.apps.dashboard2 import components
from meinberlin.apps.documents.models import Chapter

from . import views


class DocumentComponent(DashboardComponent):
    identifier = 'document_settings'
    weight = 20

    def get_menu_label(self, module):
        module_app = module.phases[0].content().app
        if module_app == 'meinberlin_documents':
            return _('Document')
        return ''

    def get_progress(self, module):
        module_app = module.phases[0].content().app
        if module_app == 'meinberlin_documents':
            if Chapter.objects.filter(module=module).exists():
                return 1, 1
            return 0, 1
        return 0, 0

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
