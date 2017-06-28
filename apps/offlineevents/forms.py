from django import forms

from apps.contrib.widgets import DateTimeInput

from . import models


class OfflineEventForm(forms.ModelForm):

    date = forms.SplitDateTimeField(
        widget=DateTimeInput(time_format='%H:%M'),
        require_all_fields=True
    )

    class Meta:
        model = models.OfflineEvent
        fields = ['name', 'date', 'description']
