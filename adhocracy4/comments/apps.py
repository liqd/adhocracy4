from django.apps import AppConfig


class CommentConfig(AppConfig):
    name = 'euth.comments'
    label = 'euth_comments'

    def ready(self):
        import euth.comments.signals  # noqa:F401
