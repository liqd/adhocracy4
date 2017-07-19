from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.contrib.widgets import DateTimeInput

from . import models


class OfflineEventForm(forms.ModelForm):

    date = forms.SplitDateTimeField(
        widget=DateTimeInput(time_format='%H:%M'),
        require_all_fields=True,
        label=_('Date')
    )

    class Meta:
        model = models.OfflineEvent
        fields = ['name', 'date', 'description']
