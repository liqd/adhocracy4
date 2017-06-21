from django.apps import AppConfig


class Config(AppConfig):
    name = 'apps.actions'
    label = 'meinberlin_actions'

    def ready(self):
        import apps.actions.signals  # noqa:F401
