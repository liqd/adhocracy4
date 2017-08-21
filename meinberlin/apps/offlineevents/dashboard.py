from django.utils.translation import ugettext_lazy as _

from meinberlin.apps.dashboard2 import DashboardComponent
from meinberlin.apps.dashboard2 import content

from . import views
from .apps import Config


class OfflineEventsComponent(DashboardComponent):
    app_label = Config.label
    label = 'offlineevents'
    identifier = 'offlineevents'

    def get_menu_label(self, project):
        return _('Offline Events')

    def get_progress(self, project):
        return 0, 0

    def get_urls(self):
        return [
            (r'^offlineevent/projects/(?P<project_slug>[-\w_]+)/$',
             views.OfflineEventListView.as_view(component=self),
             'offlineevent-list'),
            (r'^offlineevent/create/project/(?P<project_slug>[-\w_]+)/$',
             views.OfflineEventCreateView.as_view(component=self),
             'offlineevent-create'),
            (r'^offlineevent/(?P<slug>[-\w_]+)/update/$',
             views.OfflineEventUpdateView.as_view(component=self),
             'offlineevent-update'),
            (r'^offlineevent/(?P<slug>[-\w_]+)/delete/$',
             views.OfflineEventDeleteView.as_view(component=self),
             'offlineevent-delete')
        ]


content.register_project(OfflineEventsComponent())
