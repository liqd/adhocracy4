from allauth.socialaccount import providers
from django.apps import AppConfig

from .provider import ServiceKontoProvider


class Config(AppConfig):
    name = 'meinberlin.apps.servicekonto'
    label = 'meinberlin_servicekonto'

    def ready(self):
        providers.registry.register(ServiceKontoProvider)
