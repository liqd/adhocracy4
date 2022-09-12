from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components

from . import views


class VotesComponent(DashboardComponent):
    identifier = 'voting_token_export'
    weight = 48
    label = _('Voting codes')

    def is_effective(self, module):
        return module.blueprint_type == 'PB3'

    def get_progress(self, module):
        return 0, 0

    def get_base_url(self, module):
        return reverse('a4dashboard:voting-tokens', kwargs={
            'module_slug': module.slug,
        })

    def get_urls(self):
        return [
            (r'^modules/(?P<module_slug>[-\w_]+)/voting/$',
             views.VotingDashboardView.as_view(),
             'voting-tokens'),
            (r'^modules/(?P<module_slug>[-\w_]+)/voting/export-token/$',
             views.TokenExportView.as_view(),
             'token-export'),
        ]


class GenerateVotesComponent(DashboardComponent):
    identifier = 'voting_token_generation'
    weight = 49
    label = _('Generate voting codes')

    def is_effective(self, module):
        return module.blueprint_type == 'PB3'

    def get_progress(self, module):
        return 0, 0

    def get_base_url(self, module):
        return reverse('a4dashboard:voting-token-generation', kwargs={
            'module_slug': module.slug,
        })

    def get_urls(self):
        return [
            (r'^modules/(?P<module_slug>[-\w_]+)/voting-codes/$',
             views.VotingGenerationDashboardView.as_view(),
             'voting-token-generation'),
        ]


components.register_module(VotesComponent())
components.register_module(GenerateVotesComponent())
