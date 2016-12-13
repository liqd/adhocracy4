from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    name = 'adhocracy4.projects'
    label = 'a4projects'

    def ready(self):
        import adhocracy4.projects.signals  # noqa:F401
