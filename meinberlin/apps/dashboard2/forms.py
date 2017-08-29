from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from adhocracy4.categories import models as category_models
from adhocracy4.maps import models as map_models
from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models
from meinberlin.apps.contrib import widgets
from meinberlin.apps.maps.widgets import MapChoosePolygonWithPresetWidget
from meinberlin.apps.users.fields import CommaSeparatedEmailField

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


def _make_fields_required(fields, required):
    """Set the required attributes on all fields who's key is in required."""
    if required:
        for name, field in fields:
            if required == '__all__' or name in required:
                field.required = True


def _make_fields_required_for_publish(fields, required):
    """Set the required attributes on all fields who's key is in required."""
    if required:
        for name, field in fields:
            if required == '__all__' or name in required:
                field.required_for_publish = True


class ProjectDashboardForm(forms.ModelForm):
    """
    Base form for project related dashboard forms.

    Sets fields to required if the project is published.
    Intended to be used with ProjectFormComponent's.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.get_project().is_draft:
            _make_fields_required(self.fields.items(),
                                  self.get_required_fields())

        _make_fields_required_for_publish(self.fields.items(),
                                          self.get_required_fields())

    def get_project(self):
        return self.instance

    @classmethod
    def get_required_fields(cls):
        meta = getattr(cls, 'Meta', None)
        return getattr(meta, 'required_for_project_publish', [])


class ModuleDashboardForm(forms.ModelForm):
    """
    Base form for module related dashboard forms.

    Sets fields to required if the project is published.
    Intended to be used with ModuleFormComponent's.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.get_project().is_draft:
            _make_fields_required(self.fields.items(),
                                  self.get_required_fields())

        _make_fields_required_for_publish(self.fields.items(),
                                          self.get_required_fields())

    def get_project(self):
        return self.instance.project

    @classmethod
    def get_required_fields(cls):
        meta = getattr(cls, 'Meta', None)
        return getattr(meta, 'required_for_project_publish', [])


class ModuleDashboardFormSet(forms.BaseInlineFormSet):
    """
    Base form for module related dashboard formsets.

    Sets fields to required if the project is published.
    Intended to be used with ModuleFormSetComponent's.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_fields = self.get_required_fields()
        for form in self.forms:
            _make_fields_required_for_publish(form.fields.items(),
                                              required_fields)
            if not self.instance.project.is_draft:
                _make_fields_required(form.fields.items(),
                                      required_fields)

    @classmethod
    def get_required_fields(cls):
        meta = getattr(cls.form, 'Meta', None)
        return getattr(meta, 'required_for_project_publish', [])


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


class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('Category')}
    ))

    @property
    def media(self):
        media = super().media
        media.add_js(['js/formset.js'])
        return media

    class Meta:
        model = category_models.Category
        fields = ['name']


CategoryFormSet = inlineformset_factory(module_models.Module,
                                        category_models.Category,
                                        form=CategoryForm,
                                        formset=ModuleDashboardFormSet,
                                        )
