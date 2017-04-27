from django import forms
from django.forms.models import inlineformset_factory
from nested_formset import BaseNestedModelForm

from adhocracy4.modules import models as module_models
from apps.contrib.nested_formset import nestedformset_factory

from . import models


class PollForm(BaseNestedModelForm):
    class Meta:
        model = models.Poll
        fields = ['title', 'weight']
        widgets = {'weight': forms.HiddenInput()}


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = models.Choice
        fields = ['label', 'poll']


PollCollectionForm = nestedformset_factory(
    module_models.Module,
    models.Poll,
    form=PollForm,
    nested_formset=inlineformset_factory(
        models.Poll,
        models.Choice,
        form=ChoiceForm,
    )
)
