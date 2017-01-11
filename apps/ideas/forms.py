from django import forms

from . import models


class IdeaForm(forms.ModelForm):
    class Meta:
        model = models.Idea
        fields = ['name', 'description']
