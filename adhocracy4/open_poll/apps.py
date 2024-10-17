from django.apps import AppConfig


class Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "adhocracy4.open_poll"
    label = "a4open_poll"
