from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components

from . import exports
from . import views


class GenerateTokenComponent(DashboardComponent):
    identifier = 'voting_token_generation'
    weight = 48
    label = _('Code generation')
    for_superuser_only = True

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
            (r'^modules/(?P<module_slug>[-\w_]+)/generate-codes/$',
             views.TokenGenerationDashboardView.as_view(component=self),
             'voting-token-generation'),
        ]


class ExportTokenComponent(DashboardComponent):
    identifier = 'voting_token_export'
    weight = 49
    label = _('Code download')

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
            (r'^modules/(?P<module_slug>[-\w_]+)/download-codes/$',
             views.ExportTokenDashboardView.as_view(component=self),
             'voting-tokens'),
            (r'^modules/(?P<module_slug>[-\w_]+)/download-codes/export/$',
             exports.TokenExportView.as_view(),
             'token-export'),
        ]


components.register_module(GenerateTokenComponent())
components.register_module(ExportTokenComponent())
