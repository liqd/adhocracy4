from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components

from . import models
from . import views


class ActivityComponent(DashboardComponent):
    identifier = 'facetoface'
    weight = 20
    label = _('Face-to-Face Information')

    def is_effective(self, module):
        module_app = module.phases[0].content().app
        return module_app == 'meinberlin_activities'

    def get_progress(self, module):
        if models.Activity.objects.filter(module=module).exists():
            return 1, 1
        return 0, 1

    def get_base_url(self, module):
        return reverse('a4dashboard:activities-dashboard', kwargs={
            'module_slug': module.slug
        })

    def get_urls(self):
        return [(
            r'^modules/(?P<module_slug>[-\w_]+)/activities/$',
            views.ActivityDashboardView.as_view(component=self),
            'activities-dashboard'
        )]


components.register_module(ActivityComponent())
