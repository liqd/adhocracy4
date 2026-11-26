from django.apps import AppConfig


class Config(AppConfig):
    name = "adhocracy4.moderation"
    label = "a4moderation"

    def ready(self):
        from . import checks  # noqa: F401
