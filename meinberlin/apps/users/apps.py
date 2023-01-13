from django.apps import AppConfig


class Config(AppConfig):
    name = "meinberlin.apps.users"
    label = "meinberlin_users"

    def ready(self):
        import meinberlin.apps.users.signals  # noqa:F401
