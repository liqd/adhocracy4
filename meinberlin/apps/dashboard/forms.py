from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from meinberlin.apps.bplan import models as bplan_models
from meinberlin.apps.dashboard2.forms import ProjectCreateForm
from meinberlin.apps.dashboard2.forms import ProjectDashboardForm
from meinberlin.apps.datetimefield import fields as datetime_fields
from meinberlin.apps.extprojects import models as extproject_models
from meinberlin.apps.organisations.models import Organisation
from meinberlin.apps.users.fields import CommaSeparatedEmailField

User = get_user_model()


class OrganisationForm(forms.ModelForm):

    class Meta:
        model = Organisation
        fields = ['name', 'logo']
        labels = {
            'name': _('Organisation name')
        }


class ExternalProjectCreateForm(ProjectCreateForm):

    class Meta:
        model = extproject_models.ExternalProject
        fields = ['name', 'description', 'tile_image', 'tile_image_copyright']


class ExternalProjectForm(ProjectDashboardForm):

    start_date = datetime_fields.DateTimeField(
        time_format='%H:%M',
        required=False,
        require_all_fields=False,
        label=(_('Start date'), _('Start time'))
    )
    end_date = datetime_fields.DateTimeField(
        time_format='%H:%M',
        required=False,
        require_all_fields=False,
        label=(_('End date'), _('End time'))
    )

    class Meta:
        model = extproject_models.ExternalProject
        fields = ['name', 'url', 'description', 'tile_image',
                  'tile_image_copyright', 'is_archived']
        required_for_project_publish = ['name', 'url', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initial['start_date'] = self.instance.phase.start_date
        self.initial['end_date'] = self.instance.phase.end_date

    def clean_end_date(self, *args, **kwargs):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        if start_date and end_date and end_date < start_date:
            raise ValidationError(
                _('End date can not be smaller than the start date.'))
        return end_date

    def save(self, commit=True):
        project = super().save(commit)

        if commit:
            phase = project.phase
            phase.start_date = self.cleaned_data['start_date']
            phase.end_date = self.cleaned_data['end_date']
            phase.save()


class BplanProjectCreateForm(ExternalProjectCreateForm):

    class Meta:
        model = bplan_models.Bplan
        fields = ['name', 'description', 'tile_image', 'tile_image_copyright']


class BplanProjectForm(ExternalProjectForm):

    class Meta:
        model = bplan_models.Bplan
        fields = ['name', 'url', 'description', 'tile_image',
                  'tile_image_copyright', 'is_archived', 'office_worker_email']
        required_for_project_publish = ['name', 'url', 'description',
                                        'office_worker_email']


class AddUsersFromEmailForm(forms.Form):
    add_users = CommaSeparatedEmailField()

    def __init__(self, *args, **kwargs):
        # Store the label for the CommaSeparatedEmailField
        label = kwargs.pop('label', None)

        super().__init__(*args, **kwargs)

        if label:
            self.fields['add_users'].label = label

    def clean_add_users(self):
        users = []
        missing = []
        for email in self.cleaned_data['add_users']:
            try:
                user = User.objects.get(email__exact=email)
                users.append(user)
            except ObjectDoesNotExist:
                missing.append(email)

        self.missing = missing
        return users


class InviteUsersFromEmailForm(forms.Form):
    add_users = CommaSeparatedEmailField(
        label=_('Invite users via email')
    )

    def __init__(self, *args, **kwargs):
        label = kwargs.pop('label', None)
        super().__init__(*args, **kwargs)

        if label:
            self.fields['add_users'].label = label
