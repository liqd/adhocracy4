from django.apps import AppConfig


class FilesConfig(AppConfig):
    name = 'adhocracy4.files'
    label = 'a4files'

    def ready(self):
        import adhocracy4.files.signals  # noqa:F401
