from django.apps import AppConfig


class Config(AppConfig):
    name = "meinberlin.apps.plans"
    label = "meinberlin_plans"

    def ready(self):
        import meinberlin.apps.plans.signals  # noqa:F401
