from django.apps import AppConfig


class RatingsConfig(AppConfig):
    name = 'adhocracy4.ratings'
    label = 'a4ratings'

    def ready(self):
        from . import signals  # noqa:F401
