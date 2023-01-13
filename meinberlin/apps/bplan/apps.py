from django.apps import AppConfig


class Config(AppConfig):
    name = "meinberlin.apps.bplan"
    label = "meinberlin_bplan"

    def ready(self):
        import meinberlin.apps.bplan.signals  # noqa:F401
