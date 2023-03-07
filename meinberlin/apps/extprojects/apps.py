from django.apps import AppConfig


class Config(AppConfig):
    name = "meinberlin.apps.extprojects"
    label = "meinberlin_extprojects"

    def ready(self):
        import meinberlin.apps.extprojects.signals  # noqa:F401
