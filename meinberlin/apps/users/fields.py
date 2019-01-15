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
        'placeholder': 'maria@example.com, peter@example.com,…'
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
    # whitespaces, commas, semicolons or < and >.
    email_regex = re.compile(r'[^\s;,"\'<]+@[^\s;,"\'>]+\.[a-z]{2,}')
    email_validator = EmailValidator()

    def clean(self, data, initial=None):
        file = super().clean(data, initial)
        return self._extract_emails(file)

    def _extract_emails(self, file):
        if not file:
            return []

        emails = []
        for byteline in file:
            # As it is difficult to guess the correct encoding of a file,
            # email addresses are restricted to contain only ascii letters.
            # This works for every encoding which is a superset of ascii like
            # utf-8 and latin-1. Non ascii chars are simply ignored.
            line = byteline.decode('ascii', 'ignore')
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
