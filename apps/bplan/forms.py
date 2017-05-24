from django import forms

from . import models


class StatementForm(forms.ModelForm):
    class Meta:
        model = models.Statement
        fields = ['name', 'email', 'statement',
                  'street_number', 'postal_code_city']
