from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components

from . import exports
from . import views


class ExportMapIdeaComponent(DashboardComponent):
    identifier = 'mapidea_export'
    weight = 50
    label = _('Export Excel')

    def is_effective(self, module):
        module_app = module.phases[0].content().app
        return (module_app == 'meinberlin_mapideas' and
                not module.project.is_draft and not module.is_draft)

    def get_progress(self, module):
        return 0, 0

    def get_base_url(self, module):
        return reverse('a4dashboard:mapidea-export-module', kwargs={
            'module_slug': module.slug,
        })

    def get_urls(self):
        return [
            (r'^modules/(?P<module_slug>[-\w_]+)/export/mapidea/$',
             views.MapIdeaDashboardExportView.as_view(),
             'mapidea-export-module'),
            (r'^modules/(?P<module_slug>[-\w_]+)/export/mapidea/ideas/$',
             exports.MapIdeaExportView.as_view(),
             'mapidea-export'),
            (r'^modules/(?P<module_slug>[-\w_]+)/export/mapidea/comments/$',
             exports.MapIdeaCommentExportView.as_view(),
             'mapidea-comment-export'),
        ]


components.register_module(ExportMapIdeaComponent())
