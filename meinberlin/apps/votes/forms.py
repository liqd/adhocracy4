from django import forms
from django.utils.translation import gettext_lazy as _

from meinberlin.apps.votes.models import VotingToken


class VotingTokenWidget(forms.MultiWidget):

    def __init__(self, attrs=None):
        widgets = (
            forms.TextInput(attrs={'minlength': '4',
                                   'maxlength': '4'}),
            forms.TextInput(attrs={'minlength': '4',
                                   'maxlength': '4'}),
            forms.TextInput(attrs={'minlength': '4',
                                   'maxlength': '4'}),
        )
        super(VotingTokenWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value[i:i + 4] for i in range(0, len(value), 4)]
        return [None, None, None]

    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)
        return "".join(values)


class TokenForm(forms.Form):
    token = forms.CharField(widget=VotingTokenWidget())

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
            else:
                cleaned_data['token'] = token_queryset.first().token

        return cleaned_data


class TokenBatchCreateForm(forms.Form):
    number_of_tokens = forms.IntegerField(
        min_value=1,
        label=_('Number of codes needed'),
        help_text=_('Please indicate how many participants should be invited '
                    'to vote. One code will be generated per participant.')
    )
