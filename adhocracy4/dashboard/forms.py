import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.forms import RadioSelect
from django.forms import inlineformset_factory
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from adhocracy4.forms.fields import DateTimeField
from adhocracy4.maps import models as map_models
from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.phases.forms import PhaseInlineFormSet
from adhocracy4.projects import models as project_models
from adhocracy4.projects.enums import Access

from .components.forms import ModuleDashboardForm
from .components.forms import ModuleDashboardFormSet
from .components.forms import ProjectDashboardForm

User = get_user_model()


class ProjectCreateForm(forms.ModelForm):

    class Meta:
        model = project_models.Project
        fields = ['name', 'description', 'image', 'image_copyright']

    def __init__(self, organisation, creator,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.organisation = organisation
        self.creator = creator

    def save(self, commit=True):

        creator = self.creator
        org = self.organisation

        org_has_groups = hasattr(org, 'groups')
        creator_has_groups = hasattr(creator, 'groups')

        project = super().save(commit=False)
        project.organisation = self.organisation

        if org_has_groups and creator_has_groups:
            creator_groups = creator.groups.all()
            org_groups = org.groups.all()
            shared_groups = creator_groups & org_groups
            group = shared_groups.first()
            project.group = group

        if commit:
            project.save()
            project.moderators.add(self.creator)
            if hasattr(self, 'save_m2m'):
                self.save_m2m()

        return project


class ProjectBasicForm(ProjectDashboardForm):

    class Meta:
        model = project_models.Project
        fields = ['name', 'description', 'image', 'image_copyright',
                  'tile_image', 'tile_image_copyright',
                  'is_archived', 'access']
        required_for_project_publish = ['name', 'description']
        widgets = {
            'access': RadioSelect(
                choices=[
                    (Access.PUBLIC,
                     _('All users can participate (public).')),
                    (Access.PRIVATE,
                     _('Only invited users can participate (private).'))
                ]
            ),
        }


class ProjectInformationForm(ProjectDashboardForm):

    contact_heading = _('Contact for questions')
    contact_help = _('Please name a contact person. The user will '
                     'then know who is carrying out this project and '
                     'to whom they can address possible questions. '
                     'The contact person will be shown in the '
                     'information tab on the project page.')
    contact_info_label = _('More contact possibilities')

    class Meta:
        model = project_models.Project
        fields = [
            'information', 'contact_name', 'contact_address_text',
            'contact_phone', 'contact_email', 'contact_url'
        ]
        required_for_project_publish = ['information']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact_name'].widget.attrs.update(
            {'placeholder': _('Name')})
        self.fields['contact_address_text'].widget.attrs.update(
            {'placeholder': _('Address')})
        self.fields['contact_address_text'].widget.attrs['rows'] = 6
        self.fields['contact_phone'].widget.attrs.update(
            {'placeholder': _('Telephone')})
        self.fields['contact_email'].widget.attrs.update(
            {'placeholder': _('Email')})
        self.fields['contact_url'].widget.attrs.update(
            {'placeholder': _('Website')})


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

        widgets = {
            'description': forms.Textarea,
        }


class PhaseForm(forms.ModelForm):
    end_date = DateTimeField(
        time_format='%H:%M',
        time_default=datetime.time(hour=23, minute=59,
                                   tzinfo=timezone.get_default_timezone()),
        required=False,
        require_all_fields=False,
        label=(_('End date'), _('End time'))
    )
    start_date = DateTimeField(
        time_format='%H:%M',
        required=False,
        require_all_fields=False,
        label=(_('Start date'), _('Start time'))
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


class DashboardPhaseInlineFormSet(ModuleDashboardFormSet,
                                  PhaseInlineFormSet):
    pass


PhaseFormSet = inlineformset_factory(
    module_models.Module,
    phase_models.Phase,
    form=PhaseForm,
    formset=DashboardPhaseInlineFormSet,
    extra=0,
    can_delete=False,
)


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
        widgets = map_models.AreaSettings.widgets()
