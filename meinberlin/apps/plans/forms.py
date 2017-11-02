from django import forms

from . import models


class PlanForm(forms.ModelForm):

    class Meta:
        model = models.Plan
        fields = ['title', 'project', 'point']
