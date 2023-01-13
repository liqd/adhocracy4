from django.apps import AppConfig


class Config(AppConfig):
    name = "meinberlin.apps.adminlog"
    label = "meinberlin_adminlog"

    def ready(self):
        import meinberlin.apps.adminlog.signals  # noqa:F401
