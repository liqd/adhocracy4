from django.apps import AppConfig


class Config(AppConfig):
    name = 'apps.bplan'
    label = 'meinberlin_bplan'

    def ready(self):
        import apps.bplan.signals  # noqa:F401
