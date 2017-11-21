import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _


class CommaSeparatedEmailField(forms.Field):
    email_validator = EmailValidator(
        message=_('Please enter correct email addresses, separated by '
                  'commas.')
    )

    widget = widgets.TextInput(attrs={
        'placeholder': 'maria@example.com, peter@example.com, '
                       'nicola@example.com,…'
    })

    def to_python(self, value):
        if not value:
            return []

        emails = []
        for email in value.split(','):
            email = email.strip()
            self.email_validator(email)
            emails.append(email)

        return emails


class EmailFileField(forms.FileField):
    """Extract emails from uploaded text files."""

    widget = widgets.FileInput
    # Find possible email strings. Emails may be quoted and separated by
    # whitespaces, commas or semicolons.
    email_regex = re.compile(r'[^\s;,"\'<]+@[^\s;,"\'>]+\.[a-z]{2,}')
    email_validator = EmailValidator()

    def clean(self, data, initial=None):
        file = super().clean(data, initial)
        try:
            return self._extract_emails(file)
        except UnicodeDecodeError:
            raise ValidationError(_('Invalid file format.'
                                    ' Only text files are allowed.'))

    def _extract_emails(self, file):
        if not file:
            return []

        emails = []
        for byteline in file:
            line = byteline.decode('utf-8')
            for match in self.email_regex.finditer(line):
                email = match.group(0)
                if self.is_valid_email(email):
                    emails.append(email)
        return emails

    def is_valid_email(self, email):
        try:
            self.email_validator(email)
            return True
        except ValidationError:
            return False
