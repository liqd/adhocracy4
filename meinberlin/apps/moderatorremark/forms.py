from django import forms

from . import models


class ModeratorRemarkForm(forms.ModelForm):
    class Meta:
        model = models.ModeratorRemark
        fields = ["remark"]
