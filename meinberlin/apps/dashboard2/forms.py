from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models
from meinberlin.apps.contrib import widgets
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
        fields = ['name', 'description', 'image', 'tile_image', 'is_archived',
                  'is_public']
        required_for_project_publish = '__all__'


class ProjectInformationForm(ProjectDashboardForm):

    class Meta:
        model = project_models.Project
        fields = ['information']
        required_for_project_publish = '__all__'


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
        exclude = ('module', )

        widgets = {
            'type': forms.HiddenInput(),
            'weight': forms.HiddenInput()
        }
        required_for_project_publish = '__all__'


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
