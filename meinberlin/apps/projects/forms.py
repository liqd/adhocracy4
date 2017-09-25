from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from meinberlin.apps.users.fields import CommaSeparatedEmailField

from .models import ModeratorInvite
from .models import ParticipantInvite

User = get_user_model()


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


class InviteUsersFromEmailForm(forms.Form):
    add_users = CommaSeparatedEmailField(
        label=_('Invite users via email')
    )

    def __init__(self, *args, **kwargs):
        label = kwargs.pop('label', None)
        super().__init__(*args, **kwargs)

        if label:
            self.fields['add_users'].label = label
