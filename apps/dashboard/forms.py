from django import forms
from django.db.models import loading
from django.forms import modelformset_factory

from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models

from apps.contrib import multiform


def get_module_settings_form(settings_instance_or_modelref):
    if hasattr(settings_instance_or_modelref, 'module'):
        settings_model = settings_instance_or_modelref.__class__
    else:
        settings_model = loading.get_model(
            settings_instance_or_modelref[0],
            settings_instance_or_modelref[1],
        )

    class ModuleSettings(forms.ModelForm):

        class Meta:
            model = settings_model
            exclude = ['module']
            widgets = settings_model().widgets()

    return ModuleSettings


class ProjectForm(forms.ModelForm):

    class Meta:
        model = project_models.Project
        fields = ['name', 'description', 'image', 'information', 'is_public',
                  'result']

    def save(self, commit=True):
        self.instance.is_draft = 'save_draft' in self.data
        return super().save(commit)


class PhaseForm(forms.ModelForm):

    class Meta:
        model = phase_models.Phase
        exclude = ('module', )

        widgets = {
            # 'end_date': widgets.DateTimeInput(),
            # 'start_date': widgets.DateTimeInput(),
            'type': forms.HiddenInput(),
            'weight': forms.HiddenInput()
        }


class ProjectEditFormBase(multiform.MultiModelForm):

    def _project_form(self):
        return self.get_formset('project')

    def _phases_form(self):
        return self.get_formset('phases')

    def _module_settings_form(self):
        return self.get_formset('module_settings')

    def info_error_count(self):
        project_form_errors = self._project_form().errors.keys()
        info_error_count = len(project_form_errors)
        if 'result' in project_form_errors:
            info_error_count = info_error_count - 1
        return info_error_count

    def participate_error_count(self):
        module_settings_error_count = 0
        module_settings = self._module_settings_form()
        if module_settings:
            module_settings_error_count = len(module_settings.errors)
        phases_error_count = self._phases_form().total_error_count()
        return module_settings_error_count + phases_error_count

    def result_error_count(self):
        project_form_errors = self._project_form().errors.keys()
        return 1 if 'result' in project_form_errors else 0


class ProjectCreateForm(ProjectEditFormBase):

    def __init__(self, blueprint, organisation, creator, *args, **kwargs):
        kwargs['phases__queryset'] = phase_models.Phase.objects.none()
        kwargs['phases__initial'] = [
            {'phase_content': phase,
             'type': phase.identifier,
             'weight': index
             } for index, phase in enumerate(blueprint.content)
        ]

        self.organisation = organisation
        self.blueprint = blueprint
        self.creator = creator

        self.base_forms = [
            ('project', ProjectForm),
            ('phases', modelformset_factory(
                phase_models.Phase, PhaseForm,
                min_num=len(blueprint.content),
                max_num=len(blueprint.content),
            )),
        ]

        module_settings = blueprint.settings_model
        if module_settings:
            self.base_forms.append((
                'module_settings',
                get_module_settings_form(module_settings),
            ))

        return super().__init__(*args, **kwargs)

    def save(self, commit=True):
        objects = super().save(commit=False)

        project = objects['project']
        project.organisation = self.organisation
        if commit:
            project.save()
            project.moderators.add(self.creator)

        module = module_models.Module(
            name=project.slug + '_module',
            weight=1,
            project=project
        )
        objects['module'] = module
        if commit:
            module.save()

        if 'module_settings' in objects.keys():
            module_settings = objects['module_settings']
            module_settings.module = module
            if commit:
                module_settings.save()

        phases = objects['phases']

        for index, phase in enumerate(phases):
            phase.module = module
            if commit:
                phase.save()


class ProjectUpdateForm(ProjectEditFormBase):

    def __init__(self, *args, **kwargs):
        self.base_forms = [
            ('project', ProjectForm),
            ('phases', modelformset_factory(
                phase_models.Phase, PhaseForm, extra=0
            )),
        ]

        qs = kwargs['phases__queryset']
        module = qs.first().module
        if module.settings_instance:
            self.base_forms.append((
                'module_settings',
                get_module_settings_form(module.settings_instance),
            ))

        super().__init__(*args, **kwargs)

    def save(self, commit=True):

        objects = super().save(commit=False)
        project = objects['project']

        if commit:
            project.save()
            if 'module_settings' in objects:
                objects['module_settings'].save()

        cleaned_data = self._combine('cleaned_data', call=False,
                                     call_kwargs={'commit': commit})
        phases = cleaned_data['phases']
        for phase in phases:
            phase_object = phase['id']
            del phase['id']
            for key in phase:
                value = phase[key]
                setattr(phase_object, key, value)
            if commit:
                phase_object.save()
        return objects
