from django import forms
from django.core.exceptions import ValidationError

from .models import ModeratorInvite
from .models import ParticipantInvite


class InviteForm(forms.ModelForm):
    accept = forms.CharField(required=False)
    reject = forms.CharField(required=False)

    def clean(self):
        data = self.data
        if 'accept' not in data and 'reject' not in data:
            raise ValidationError('Reject or accept')
        return data

    def is_accepted(self):
        data = self.data
        return 'accept' in data and 'reject' not in data


class ParticipantInviteForm(InviteForm):

    class Meta:
        model = ParticipantInvite
        fields = ['accept', 'reject']


class ModeratorInviteForm(InviteForm):

    class Meta:
        model = ModeratorInvite
        fields = ['accept', 'reject']
