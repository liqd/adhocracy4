from adhocracy4.modules import views as module_views

from . import models


class OfflineEventDetailView(module_views.ItemDetailView):
    model = models.OfflineEvent
    permission_required = 'meinberlin_offlineevents.view_offlineevent'

    @property
    def project(self):
        return self.get_object().project
