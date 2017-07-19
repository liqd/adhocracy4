from django.apps import AppConfig


class Config(AppConfig):
    name = 'apps.notifications'
    label = 'meinberlin_notifications'

    def ready(self):
        import apps.notifications.signals  # noqa:F401
