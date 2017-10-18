from django import forms

from . import models


class ModeratorStatementForm(forms.ModelForm):
    class Meta:
        model = models.ModeratorStatement
        fields = ['statement']
