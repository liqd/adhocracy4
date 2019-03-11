import collections

from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ngettext
from django.utils.translation import ugettext_lazy as _

from meinberlin.apps.organisations.models import Organisation

User = get_user_model()


class UserAdminForm(auth_forms.UserChangeForm):

    def clean(self):
        groups = self.cleaned_data.get('groups')
        group_list = groups.values_list('id', flat=True)
        group_organisations = Organisation.objects\
            .filter(groups__in=group_list)\
            .values_list('name', flat=True)
        duplicates = [item for item, count
                      in collections.Counter(group_organisations).items()
                      if count > 1]
        if duplicates:
            count = len(duplicates)
            message = ngettext(
                'User is member in more then one group '
                'in this organisation: %(duplicates)s.',
                'User is member in more then one group '
                'in these organisations: %(duplicates)s.',
                count) % {
                'duplicates': ', '.join(duplicates)
            }
            raise ValidationError(message)
        return self.cleaned_data


class TermsSignupForm(auth_forms.UserCreationForm):
    terms_of_use = forms.BooleanField(label=_('Terms of use'), error_messages={
        'required': _('Please accept the terms of use.')
    })

    def signup(self, request, user):

        # without the allaouth plugin, this would typically be inside .save
        user.get_newsletters = self.cleaned_data["get_newsletters"]

        user.signup(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
        )

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2',
                  'get_newsletters', 'terms_of_use')
