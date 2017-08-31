from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from meinberlin.apps.dashboard2 import DashboardComponent
from meinberlin.apps.dashboard2 import components

from . import get_exports
from . import views


class ExportModuleComponent(DashboardComponent):
    identifier = 'module_export'
    weight = 50

    def is_effective(self, module):
        return not module.project.is_draft and get_exports(module)

    def get_menu_label(self, module):
        return _('Export')

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
