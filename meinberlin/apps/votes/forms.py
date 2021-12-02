from django import forms
from django.utils.translation import gettext_lazy as _

from meinberlin.apps.votes.models import VotingToken


class TokenForm(forms.Form):

    token = forms.CharField(max_length=40)

    def __init__(self, *args, **kwargs):
        self.module_id = kwargs.pop('module_id')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if 'token' in self.cleaned_data:
            token_queryset = VotingToken.objects.filter(
                token=self.cleaned_data['token'],
                module_id=self.module_id
            )
            if not token_queryset:
                self.add_error('token', _('This token is not valid'))

        return cleaned_data
