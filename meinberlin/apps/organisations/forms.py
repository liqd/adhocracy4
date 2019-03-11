import collections

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ngettext

from meinberlin.apps.users.models import User

from . import models


class OrganisationForm(forms.ModelForm):

    class Meta:
        model = models.Organisation
        fields = '__all__'

    def clean(self):
        groups = self.cleaned_data.get('groups')
        group_list = groups.values_list('id', flat=True)
        group_users = User.objects\
            .filter(groups__in=group_list)\
            .values_list('email', flat=True)
        duplicates = [item for item, count
                      in collections.Counter(group_users).items()
                      if count > 1]
        if duplicates:
            count = len(duplicates)
            message = ngettext(
                '%(duplicates)s is member of several '
                'groups in that organisation.',
                '%(duplicates)s are member of several '
                'groups in that organisation.',
                count) % {
                'duplicates': ', '.join(duplicates)
            }
            raise ValidationError(message)
        return self.cleaned_data
