from django.db import models
from django.utils.translation import ugettext_lazy as _


class ModeratorFeedbackField(models.CharField):
    description = _("Moderator feedback for items with fixed feedback choices")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 254
        kwargs['null'] = True
        kwargs['default'] = None
        kwargs['blank'] = True
        super(ModeratorFeedbackField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        """Initialize choices from the enclosing model.

        This is called in the context of the enclosing model
        from which it may receive the feedback choices.
        """
        # Get the feedback choices as defined in the model
        if hasattr(cls, 'moderator_feedback_choices'):
            self.choices = cls.moderator_feedback_choices

        # Call the super method at last so that choices are already initialized
        super(ModeratorFeedbackField, self) \
            .contribute_to_class(cls, name, **kwargs)
