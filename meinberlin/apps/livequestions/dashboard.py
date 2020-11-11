from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components

from . import views


class LiveStreamComponent(DashboardComponent):
    identifier = 'live_stream'
    weight = 20
    label = _('Live Stream')

    def is_effective(self, module):
        module_app = module.phases[0].content().app
        return (module_app == 'meinberlin_livequestions')

    def get_progress(self, module):
        return 0, 0

    def get_base_url(self, module):
        return reverse('a4dashboard:livequestions-livestream', kwargs={
            'module_slug': module.slug,
        })

    def get_urls(self):
        return [(
            r'^modules/(?P<module_slug>[-\w_]+)/livestream/$',
            views.LiveStreamDashboardView.as_view(component=self),
            'livequestions-livestream'
        )]


components.register_module(LiveStreamComponent())
