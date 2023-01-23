from django import forms
from django.forms.widgets import TextInput
from django.utils.translation import gettext_lazy as _

from meinberlin.apps.votes.models import VotingToken


class VotingTokenField(forms.CharField):
    def __init__(self, placeholder=None, *args, **kwargs):
        widget = TextInput(
            attrs={
                "class": "form-control",
                "minlength": 12,
                "maxlength": 14,
                "placeholder": placeholder,
            }
        )
        super().__init__(widget=widget, *args, **kwargs)

    default_error_messages = {
        "invalid_short": _("The token is too short"),
        "invalid_long": _("The token is too long"),
    }

    def clean(self, value):

        # ensure no spaces or dashes
        value = value.replace(" ", "").replace("-", "")

        # check the value is not too short or too long
        if len(value) < 12:
            raise forms.ValidationError(self.error_messages["invalid_short"])
        elif len(value) > 12:
            raise forms.ValidationError(self.error_messages["invalid_long"])

        return value


class TokenForm(forms.Form):
    token = VotingTokenField(placeholder="0000-0000-0000")

    def __init__(self, *args, **kwargs):
        self.module_id = kwargs.pop("module_id")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if "token" in self.cleaned_data:
            token = VotingToken.get_voting_token(
                token=self.cleaned_data["token"], module_id=self.module_id
            )
            if not token:
                self.add_error("token", _("This token is not valid"))
            else:
                cleaned_data["token"] = token.token_hash

        return cleaned_data


class TokenBatchCreateForm(forms.Form):
    number_of_tokens = forms.IntegerField(
        min_value=1,
        label=_("Number of codes needed"),
        help_text=_(
            "Please indicate how many participants should be invited "
            "to vote. One code will be generated per participant."
        ),
    )
