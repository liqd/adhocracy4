from django import forms

from . import models


class LiveStreamForm(forms.ModelForm):
    class Meta:
        model = models.LiveStream
        fields = ['live_stream']
