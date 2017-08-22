from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models

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


class ProjectUpdateForm(forms.ModelForm):

    class Meta:
        model = project_models.Project
        fields = ['name', 'description', 'image', 'tile_image', 'information',
                  'result', 'is_archived', 'is_public']
        labels = {
            'is_public': _('This project is public.')
        }


def _make_fields_required(fields, required):
    """Set the required attributes on all fields who's key is in required."""
    if required:
        for name, field in fields:
            if required == '__all__' or name in required:
                field.required = True


class ProjectDashboardForm(forms.ModelForm):
    """
    Base form for project related dashboard forms.

    Sets fields to required if the project is published.
    Intended to be used with ProjectFormComponent's.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.is_draft:
            _make_fields_required(self.fields.items(),
                                  self.get_required_fields())

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

        if not self.instance.project.is_draft:
            _make_fields_required(self.fields.items(),
                                  self.get_required_fields())

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

        if not self.instance.project.is_draft:
            required_fields = self.get_required_fields()
            for form in self.forms:
                _make_fields_required(form.fields.items(),
                                      required_fields)

    @classmethod
    def get_required_fields(cls):
        meta = getattr(cls.form, 'Meta', None)
        return getattr(meta, 'required_for_project_publish', [])


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


class ModuleBasicForm(ModuleDashboardForm):

    class Meta:
        model = module_models.Module
        fields = ['name', 'description']
        required_for_project_publish = '__all__'


class PhaseForm(forms.ModelForm):

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
