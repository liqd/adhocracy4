from django import forms

from adhocracy4.categories.forms import CategorizableFieldMixin

from . import models


class IdeaForm(CategorizableFieldMixin, forms.ModelForm):
    right_of_use = forms.BooleanField()

    class Meta:
        model = models.Idea
        fields = ['name', 'description', 'image', 'category']


class IdeaModerateForm(forms.ModelForm):
    class Meta:
        model = models.Idea
        fields = ['moderator_feedback']
