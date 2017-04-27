from django import forms
from django.forms.models import inlineformset_factory
from nested_formset import BaseNestedModelForm

from apps.contrib.nested_formset import nestedformset_factory

from . import models


class QuestionForm(BaseNestedModelForm):
    class Meta:
        model = models.Question
        fields = ['label', 'weight']
        widgets = {'weight': forms.HiddenInput()}


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = models.Choice
        fields = ['label', 'question']


PollForm = nestedformset_factory(
    models.Poll,
    models.Question,
    form=QuestionForm,
    nested_formset=inlineformset_factory(
        models.Question,
        models.Choice,
        form=ChoiceForm,
    )
)
