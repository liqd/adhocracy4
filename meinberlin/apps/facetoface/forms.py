from django import forms

from . import models


class ActivityForm(forms.ModelForm):

    class Meta:
        model = models.Activity
        fields = ['name', 'highlight', 'description']
