from django.conf import settings
from django.db import models


class TopicField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 254
        kwargs['default'] = ''
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        """
        Initialize the choices from the project's settings if they exist.
        """
        if hasattr(settings, 'A4_PROJECT_TOPICS'):
            self.choices = settings.A4_PROJECT_TOPICS

        # Call the super method at last so that choices are already initialized
        super().contribute_to_class(cls, name, **kwargs)
