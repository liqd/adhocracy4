from django import forms
from django.utils.translation import ugettext_lazy as _


class InitiatorRequestForm(forms.Form):
    organisation_name = forms.CharField(label=_('Name of the organisation'))
    phone = forms.CharField(label=_('Phone number'))
