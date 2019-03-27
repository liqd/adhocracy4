from django import forms
from django.utils.translation import ugettext_lazy as _

from meinberlin.apps.organisations.models import Organisation


class OrganisationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].required = True
        self.fields['url'].required = True
        self.fields['url'].help_text = _('Please enter '
                                         'a full url which '
                                         'starts with https:// '
                                         'or http://')

    class Meta:
        model = Organisation
        fields = ['name', 'logo', 'address', 'url']
        labels = {
            'name': _('Organisation name')
        }
