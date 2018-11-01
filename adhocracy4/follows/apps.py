from django.apps import AppConfig


class Config(AppConfig):
    name = 'adhocracy4.follows'
    label = 'a4follows'

    def ready(self):
        import adhocracy4.follows.signals  # noqa:F401
