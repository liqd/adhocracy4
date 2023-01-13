from django import forms

from . import models


class ModeratorFeedbackForm(forms.ModelForm):
    class Meta:
        model = models.ModeratorFeedback
        fields = ["feedback_text"]
