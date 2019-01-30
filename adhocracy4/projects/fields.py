from django.conf import settings
from multiselectfield import MultiSelectField


class TopicField(MultiSelectField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 254
        kwargs['max_choices'] = 2
        kwargs['default'] = ''
        kwargs['blank'] = False
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        """
        Initialize the choices from the project's settings if they exist.
        """
        if hasattr(settings, 'A4_PROJECT_TOPICS'):
            self.choices = settings.A4_PROJECT_TOPICS

        # Call the super method at last so that choices are already initialized
        super().contribute_to_class(cls, name, **kwargs)
