from django.apps import AppConfig


class Config(AppConfig):
    name = 'adhocracy4.comments'
    label = 'a4comments'

    def ready(self):
        import adhocracy4.comments.signals  # noqa:F401
