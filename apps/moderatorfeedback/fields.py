import re
import unicodedata

from django.core import checks
from django.core.exceptions import FieldError
from django.db import models
from django.utils.encoding import force_text
from django.utils.functional import curry
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class ModeratorFeedbackField(models.CharField):
    description = _("")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 254
        kwargs['null'] = True
        kwargs['default'] = None
        kwargs['blank'] = True
        super(ModeratorFeedbackField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = \
            super(ModeratorFeedbackField, self).deconstruct()
        del kwargs['max_length']
        del kwargs['null']
        del kwargs['default']
        del kwargs['blank']
        # del kwargs["choices"]
        return name, path, args, kwargs

    def check(self, **kwargs):
        errors = super(ModeratorFeedbackField, self).check(**kwargs)
        errors.extend(self._check_choices_attribute(**kwargs))
        return errors

    def _check_choices_attribute(self, **kwargs):
        try:
            choices = self.choices
            if len(choices) == 0:
                raise ValueError()
        except TypeError:
            return [
                checks.Error(
                    "ModeratorFeedbackField must define a 'choices' "
                    "attribute.",
                    hint=None,
                    obj=self,
                    id='fields.E???',  # how to choose the error id?
                )
            ]
        except ValueError:
            return [
                checks.Error(
                    "'choices' may not be empty.",
                    hint=None,
                    obj=self,
                    id='fields.E???',  # how to choose the error id?
                )
            ]
        else:
            return []

    def contribute_to_class(self, cls, name, **kwargs):
        """
        Add field specific attributes to the enclosing model.

        This method is called in the context of the enclosing
        model. It is used to set field specific attributes on
        the model. For example it is used to set the generic
        model.get_XXX_display methods for the choice fields.
        In this case it is used to make the moderator feedback
        context available.
        """
        super(ModeratorFeedbackField, self) \
            .contribute_to_class(cls, name, **kwargs)

        if hasattr(cls, 'get_moderator_feedback'):
            raise FieldError(
                'Only one %r is allowed per model.' % (
                    self.__class___.__name__
                ))
        setattr(cls, 'get_moderator_feedback',
                curry(self._get_moderator_feedback, field=self))

    @staticmethod
    def _get_moderator_feedback(model, field):
        value = getattr(model, field.attname)
        display = force_text(
            dict(field.flatchoices).get(value, value),
            strings_only=True)
        value_class = classify(value)

        return {
            'value': value,
            'display': display,
            'value_class': value_class
        }


def classify(value):
    """
    Create a valid CSS class name from a value.

    Converts to ASCII. Converts spaces to dashes. Removes characters that
    aren't alphanumerics, underscores, or hyphens.
    Also strips leading and trailing whitespace.
    """
    if value is None:
        return 'NONE'

    value = force_text(value)
    value = unicodedata.normalize('NFKD', value) \
        .encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip()
    return mark_safe(re.sub('[-\s]+', '-', value))
