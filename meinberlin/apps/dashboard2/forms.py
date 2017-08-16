from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from adhocracy4.categories import models as category_models
from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models
from meinberlin.apps.contrib import multiform

User = get_user_model()


class ProjectEditFormBase(multiform.MultiModelForm):

    def _project_form(self):
        return self.get_formset('project')

    def _phases_form(self):
        return self.get_formset('phases')

    def _categories_form(self):
        return self.get_formset('categories')

    def _module_settings_form(self):
        return self.get_formset('module_settings')

    def info_error_count(self):
        project_form_errors = self._project_form().errors.keys()
        info_error_count = len(project_form_errors)
        if 'result' in project_form_errors:
            info_error_count = info_error_count - 1

        return info_error_count

    def participate_error_count(self):
        error_count = 0

        module_settings = self._module_settings_form()
        if module_settings is not None:
            error_count += len(module_settings.errors)

        categories = self._categories_form()
        if categories is not None:
            error_count += categories.total_error_count()

        error_count += self._phases_form().total_error_count()

        return error_count

    def result_error_count(self):
        project_form_errors = self._project_form().errors.keys()
        return 1 if 'result' in project_form_errors else 0

    def _show_categories_form(self, phases):
        """Check if any of the phases has a categorizable item.

        TODO: Move this functionality to a4phases.
        """
        for phase in phases:
            for models in phase.features.values():
                for model in models:
                    if category_models.Categorizable.is_categorizable(model):
                        return True


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


class ProjectBasicForm(forms.ModelForm):

    class Meta:
        model = project_models.Project
        fields = ['name', 'description', 'image', 'tile_image', 'is_archived',
                  'is_public']


class ProjectInformationForm(forms.ModelForm):

    class Meta:
        model = project_models.Project
        fields = ['information']


class ModuleBasicForm(forms.ModelForm):

    class Meta:
        model = module_models.Module
        fields = ['name', 'description']


class PhaseForm(forms.ModelForm):

    class Meta:
        model = phase_models.Phase
        exclude = ('module', )

        widgets = {
            'type': forms.HiddenInput(),
            'weight': forms.HiddenInput()
        }


PhaseFormSet = inlineformset_factory(module_models.Module,
                                     phase_models.Phase,
                                     form=PhaseForm,
                                     extra=0,
                                     can_delete=False,
                                     )
