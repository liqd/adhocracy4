from django.apps import AppConfig


class FollowsConfig(AppConfig):
    name = 'euth.follows'
    label = 'euth_follows'

    def ready(self):
        import euth.follows.signals  # noqa:F401
