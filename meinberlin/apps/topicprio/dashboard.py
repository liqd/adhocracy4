from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from meinberlin.apps.dashboard2 import DashboardComponent
from meinberlin.apps.dashboard2 import components

from . import models
from . import views


class TopicEditComponent(DashboardComponent):
    identifier = 'topic_edit'
    weight = 20
    label = _('Topics')

    def is_effective(self, module):
        module_app = module.phases[0].content().app
        return module_app == 'meinberlin_topicprio'

    def get_progress(self, module):
        if models.Topic.objects.filter(module=module).exists():
            return 1, 1
        return 0, 1

    def get_base_url(self, module):
        return reverse('a4dashboard:topic-list', kwargs={
            'module_slug': module.slug
        })

    def get_urls(self):
        return [
            (r'^topics/module/(?P<module_slug>[-\w_]+)/$',
             views.TopicListDashboardView.as_view(component=self),
             'topic-list'),
            (r'^topics/create/module/(?P<module_slug>[-\w_]+)/$',
             views.TopicCreateView.as_view(component=self),
             'topic-create'),
            (r'^topics/(?P<year>\d{4})-(?P<pk>\d+)/update/$',
             views.TopicUpdateView.as_view(component=self),
             'topic-update'),
            (r'^topics/(?P<year>\d{4})-(?P<pk>\d+)/delete/$',
             views.TopicDeleteView.as_view(component=self),
             'topic-delete')
        ]


components.register_module(TopicEditComponent())
