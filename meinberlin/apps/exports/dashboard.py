from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components

from . import exports
from . import views


class ExportModuleComponent(DashboardComponent):
    identifier = 'module_export'
    weight = 50
    label = _('Export Excel')

    def is_effective(self, module):
        return not module.project.is_draft and module in exports

    def get_progress(self, module):
        return 0, 0

    def get_base_url(self, module):
        return reverse('a4dashboard:export-module', kwargs={
            'module_slug': module.slug,
            'export_id': 0,
        })

    def get_urls(self):
        return [
            (r'^modules/(?P<module_slug>[-\w_]+)/export/(?P<export_id>\d+)/$',
             views.ExportModuleDispatcher.as_view(),
             'export-module'),
        ]


components.register_module(ExportModuleComponent())
