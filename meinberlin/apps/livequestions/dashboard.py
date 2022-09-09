from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import ModuleFormSetComponent
from adhocracy4.dashboard import components

from . import forms
from . import views


class LiveStreamComponent(DashboardComponent):
    identifier = 'live_stream'
    weight = 20
    label = _('Livestream')

    def is_effective(self, module):
        return module.blueprint_type == 'IE'

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


class ModuleAffiliationsComponent(ModuleFormSetComponent):
    identifier = 'affiliations'
    weight = 13
    label = _('Affiliations')

    form_title = _('Edit affiliations')
    form_class = forms.AffiliationFormSet
    form_template_name = \
        'meinberlin_livequestions/includes/module_affiliations_form.html'

    def is_effective(self, module):
        return module.blueprint_type == 'IE'


components.register_module(LiveStreamComponent())
components.register_module(ModuleAffiliationsComponent())
