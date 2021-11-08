from django import forms
from django.apps import apps
from django.conf import settings
from django.utils.translation import gettext_lazy as _

Organisation = apps.get_model(settings.A4_ORGANISATIONS_MODEL)


class InitiatorRequestForm(forms.Form):
    organisation = forms.ModelChoiceField(
        label=_('Organisation'),
        queryset=Organisation.objects.all(),
        required=True,
        empty_label=None
    )

    phone = forms.CharField(label=_('Phone number'))
