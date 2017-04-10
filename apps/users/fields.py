import re
from django.core.validators import RegexValidator
from django.forms.fields import Field
from django.forms.widgets import Textarea


class CommaSeparatedEmailField(Field):
    default_validators = [RegexValidator(
        # a list of emails, separated by commas with optional space after
        regex=r'^([^@]+@[^@\s]+\.[^@\s,]+((,\s?)|$))+$',
        # message=_('Please enter correct e-mail addresses, separated by '
        #          'commas.')
    )]

    widget = Textarea(attrs={
        'placeholder': 'jana@beispiel.de, tobias@beispiel.de, '
                       'swetlana@beispiel.de,…'
    })

    def to_python(self, value):
        emails_str = value.strip(' ,')
        return re.split(r',\s?', emails_str)
