from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from meinberlin.apps.dashboard2 import DashboardComponent
from meinberlin.apps.dashboard2 import components

from . import models
from . import views


class MapTopicEditComponent(DashboardComponent):
    identifier = 'map_topic_edit'
    weight = 20
    label = _('Topics')

    def is_effective(self, module):
        module_app = module.phases[0].content().app
        return module_app == 'meinberlin_maptopicprio'

    def get_progress(self, module):
        if models.MapTopic.objects.filter(module=module).exists():
            return 1, 1
        return 0, 1

    def get_base_url(self, module):
        return reverse('a4dashboard:topic-list', kwargs={
            'module_slug': module.slug
        })

    def get_urls(self):
        return [
            (r'^maptopics/module/(?P<module_slug>[-\w_]+)/$',
             views.MapTopicListDashboardView.as_view(component=self),
             'maptopic-list'),
            (r'^maptopics/create/module/(?P<module_slug>[-\w_]+)/$',
             views.MapTopicCreateView.as_view(component=self),
             'maptopic-create'),
            (r'^maptopics/(?P<slug>[-\w_]+)/update/$',
             views.MapTopicUpdateView.as_view(component=self),
             'maptopic-update'),
            (r'^maptopics/(?P<slug>[-\w_]+)/delete/$',
             views.MapTopicDeleteView.as_view(component=self),
             'maptopic-delete')
        ]


components.register_module(MapTopicEditComponent())
