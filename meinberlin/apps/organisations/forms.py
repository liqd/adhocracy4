import collections

from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from adhocracy4.projects.models import Project
from meinberlin.apps.plans.models import Plan
from meinberlin.apps.users.models import User

from . import models


class OrganisationForm(forms.ModelForm):

    class Meta:
        model = models.Organisation
        fields = '__all__'
        widgets = {
            'groups': widgets.FilteredSelectMultiple(_('Groups'), False),
        }

    def clean(self):
        groups = self.cleaned_data.get('groups')
        duplicates = self._check_user_twice(groups)
        if duplicates:
            raise ValidationError(
                self._get_duplicate_error_message(duplicates))
        if self.instance.id:
            old_groups = self._get_old_groups(groups)
            self._delete_from_old_groups(old_groups)
        return self.cleaned_data

    def _get_old_groups(self, groups):
        instance_groups = self.instance.groups.all()
        if instance_groups:
            form_groups = groups
            return instance_groups.exclude(id__in=[
                group.id for group in form_groups
            ])
        return Group.objects.none()

    def _check_user_twice(self, groups):
        group_list = groups.values_list('id', flat=True)
        group_users = User.objects \
            .filter(groups__in=group_list) \
            .values_list('email', flat=True)
        duplicates = [item for item, count
                      in collections.Counter(group_users).items()
                      if count > 1]
        return duplicates

    def _get_duplicate_error_message(self, duplicates):
        count = len(duplicates)
        return ngettext(
            '%(duplicates)s is member of several '
            'groups in that organisation.',
            '%(duplicates)s are member of several '
            'groups in that organisation.',
            count) % {'duplicates': ', '.join(duplicates)}

    def _delete_from_old_groups(self, old_groups):
        if old_groups:
            group_ids = old_groups.values_list('id', flat=True)
            plans = Plan.objects.filter(group_id__in=group_ids)
            projects = Project.objects.filter(group_id__in=group_ids)
            plans.update(group=None)
            projects.update(group=None)
