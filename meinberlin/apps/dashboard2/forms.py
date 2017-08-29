from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from adhocracy4.maps import models as map_models
from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models
from meinberlin.apps.bplan import models as bplan_models
from meinberlin.apps.contrib import widgets
from meinberlin.apps.extprojects import models as extproject_models
from meinberlin.apps.maps.widgets import MapChoosePolygonWithPresetWidget
from meinberlin.apps.users.fields import CommaSeparatedEmailField

from .components.forms import ModuleDashboardForm
from .components.forms import ModuleDashboardFormSet
from .components.forms import ProjectDashboardForm

User = get_user_model()


class ProjectCreateForm(forms.ModelForm):

    class Meta:
        model = project_models.Project
        fields = ['name', 'description', 'image', ]

    def __init__(self, type, organisation, creator,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = type
        self.organisation = organisation
        self.creator = creator

    def save(self, commit=True):
        project = super().save(commit=False)

        project.typ = self.type
        project.organisation = self.organisation
        project.creator = self.creator

        if commit:
            project.save()
            if hasattr(self, 'save_m2m'):
                self.save_m2m()

        return project


class ProjectBasicForm(ProjectDashboardForm):

    class Meta:
        model = project_models.Project
        fields = ['name', 'description', 'image', 'tile_image',
                  'is_archived', 'is_public']
        required_for_project_publish = ['name', 'description']


class ProjectInformationForm(ProjectDashboardForm):

    class Meta:
        model = project_models.Project
        fields = ['information']
        required_for_project_publish = ['information']


class ProjectResultForm(ProjectDashboardForm):

    class Meta:
        model = project_models.Project
        fields = ['result']
        required_for_project_publish = []


class ModuleBasicForm(ModuleDashboardForm):

    class Meta:
        model = module_models.Module
        fields = ['name', 'description']
        required_for_project_publish = '__all__'


class PhaseForm(forms.ModelForm):
    end_date = forms.SplitDateTimeField(
        widget=widgets.DateTimeInput(time_format='%H:%M'),
        require_all_fields=True,
        label=_('End date')
    )
    start_date = forms.SplitDateTimeField(
        widget=widgets.DateTimeInput(time_format='%H:%M'),
        require_all_fields=True,
        label=_('Start date')
    )

    class Meta:
        model = phase_models.Phase
        fields = ['name', 'description', 'start_date', 'end_date',
                  'type',  # required for get_phase_name in the tpl
                  ]
        required_for_project_publish = ['name', 'description', 'start_date',
                                        'end_date']
        widgets = {
            'type': forms.HiddenInput(),
            'weight': forms.HiddenInput()
        }


PhaseFormSet = inlineformset_factory(module_models.Module,
                                     phase_models.Phase,
                                     form=PhaseForm,
                                     formset=ModuleDashboardFormSet,
                                     extra=0,
                                     can_delete=False,
                                     )


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


# meinBerlin related Forms

class ExternalProjectCreateForm(ProjectCreateForm):

    class Meta:
        model = extproject_models.ExternalProject
        fields = ['name', 'description', 'tile_image', ]


class ExternalProjectForm(ProjectDashboardForm):

    start_date = forms.SplitDateTimeField(
        required=False,
        widget=widgets.DateTimeInput(time_format='%H:%M'),
        label=_('Start date')
    )
    end_date = forms.SplitDateTimeField(
        required=False,
        widget=widgets.DateTimeInput(time_format='%H:%M'),
        label=_('End date')
    )

    class Meta:
        model = extproject_models.ExternalProject
        fields = ['name', 'url', 'description', 'tile_image', 'is_archived']
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
        fields = ['name', 'description', 'tile_image', ]


class BplanProjectForm(ExternalProjectForm):

    class Meta:
        model = bplan_models.Bplan
        fields = ['name', 'url', 'description', 'tile_image', 'is_archived',
                  'office_worker_email']
        required_for_project_publish = ['name', 'url', 'description',
                                        'office_worker_email']


class AreaSettingsForm(ModuleDashboardForm):

    def __init__(self, *args, **kwargs):
        self.module = kwargs['instance']
        kwargs['instance'] = self.module.settings_instance
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        super().save(commit)
        return self.module

    def get_project(self):
        return self.module.project

    class Meta:
        model = map_models.AreaSettings
        fields = ['polygon']
        required_for_project_publish = ['polygon']
        # widgets = map_models.AreaSettings.widgets()
        widgets = {'polygon': MapChoosePolygonWithPresetWidget}
