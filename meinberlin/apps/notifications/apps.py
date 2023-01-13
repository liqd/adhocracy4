from django.apps import AppConfig


class Config(AppConfig):
    name = "meinberlin.apps.notifications"
    label = "meinberlin_notifications"

    def ready(self):
        import meinberlin.apps.notifications.signals  # noqa:F401
