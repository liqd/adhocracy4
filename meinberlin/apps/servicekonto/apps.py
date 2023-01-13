from allauth.socialaccount import providers
from django.apps import AppConfig


class Config(AppConfig):
    name = "meinberlin.apps.servicekonto"
    label = "meinberlin_servicekonto"

    def ready(self):
        from .provider import ServiceKontoProvider

        providers.registry.register(ServiceKontoProvider)
