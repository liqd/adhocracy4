from django.apps import AppConfig


class Config(AppConfig):
    name = 'adhocracy4.images'
    label = 'a4images'

    def ready(self):
        import adhocracy4.images.signals  # noqa:F401
