from django import forms
from django.contrib import admin

from . import content
from . import models


class PhaseForm(forms.ModelForm):
    type = forms.ChoiceField(choices=content.as_choices)

    class Meta:
        fields = '__all__'
        model = models.Phase


class PhaseInline(admin.TabularInline):
    model = models.Phase
    form = PhaseForm
    extra = 0
    min_num = 1
