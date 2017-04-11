import re
from django.core.validators import RegexValidator
from django.forms.fields import Field
from django.forms.widgets import Input
from django.utils.translation import ugettext as _


class CommaSeparatedEmailField(Field):
    default_validators = [RegexValidator(
        # a list of emails, separated by commas with optional space after
        regex=r'^([^@]+@[^@\s]+\.[^@\s,]+((,\s?)|$))+$',
        message=_('Please enter correct e-mail addresses, separated by '
                  'commas.')
    )]

    widget = Input(attrs={
        'placeholder': 'maria@beispiel.de, peter@beispiel.de, '
                       'nicola@beispiel.de,…'
    })

    def to_python(self, value):
        emails_str = value.strip(' ,')
        return re.split(r',\s?', emails_str)
