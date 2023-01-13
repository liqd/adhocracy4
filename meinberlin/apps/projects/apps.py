from django.apps import AppConfig


class Config(AppConfig):
    name = "meinberlin.apps.projects"
    label = "meinberlin_projects"

    def ready(self):
        from . import overwrites

        overwrites.overwrite_access_enum_label()
