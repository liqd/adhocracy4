from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components

from . import models
from . import views


class PollComponent(DashboardComponent):
    identifier = 'polls'
    weight = 20
    label = _('Poll')

    def is_effective(self, module):
        module_app = module.phases[0].content().app
        return module_app == 'a4polls'

    def get_progress(self, module):
        if models.Question.objects.filter(poll__module=module).exists():
            return 1, 1
        return 0, 1

    def get_base_url(self, module):
        return reverse('a4dashboard:poll-dashboard', kwargs={
            'module_slug': module.slug
        })

    def get_urls(self):
        return [(
            r'^modules/(?P<module_slug>[-\w_]+)/poll/$',
            views.PollDashboardView.as_view(component=self),
            'poll-dashboard'
        )]


components.register_module(PollComponent())
