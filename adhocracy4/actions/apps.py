from django.apps import AppConfig


class Config(AppConfig):
    name = 'adhocracy4.actions'
    label = 'a4actions'

    def ready(self):
        import adhocracy4.actions.signals  # noqa:F401
