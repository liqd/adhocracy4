from django import forms
from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from django.utils.translation import ugettext_lazy as _

from adhocracy4.categories import models as category_models
from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models
from meinberlin.apps.bplan import models as bplan_models
from meinberlin.apps.bplan import phases as bplan_phases
from meinberlin.apps.contrib import multiform
from meinberlin.apps.contrib import widgets
from meinberlin.apps.contrib.formset import dynamic_modelformset_factory
from meinberlin.apps.extprojects import models as extproject_models
from meinberlin.apps.extprojects import phases as extproject_phases
from meinberlin.apps.maps.widgets import MapChoosePolygonWithPresetWidget
from meinberlin.apps.organisations.models import Organisation
from meinberlin.apps.users.fields import CommaSeparatedEmailField

User = get_user_model()


def get_module_settings_form(settings_instance_or_modelref):
    if hasattr(settings_instance_or_modelref, 'module'):
        settings_model = settings_instance_or_modelref.__class__
    else:
        settings_model = apps.get_model(
            settings_instance_or_modelref[0],
            settings_instance_or_modelref[1],
        )

    setting_widgets = settings_model.widgets()

    # overwrite MapChoosePolygonWidget
    if 'polygon' in setting_widgets:
        setting_widgets['polygon'] = MapChoosePolygonWithPresetWidget

    class ModuleSettings(forms.ModelForm):

        class Meta:
            model = settings_model
            exclude = ['module']
            widgets = setting_widgets

    return ModuleSettings


class ProjectForm(forms.ModelForm):

    class Meta:
        model = project_models.Project
        fields = ['name', 'description', 'image', 'tile_image', 'information',
                  'result', 'is_archived', 'is_public']
        labels = {
            'is_public': _('This project is public.')
        }


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


class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('Category')}
    ))

    class Meta:
        model = category_models.Category
        exclude = ('module',)


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
        return False


class ProjectCreateForm(ProjectEditFormBase):

    def __init__(self, blueprint, blueprint_key, organisation, creator,
                 *args, **kwargs):
        kwargs['phases__queryset'] = phase_models.Phase.objects.none()
        kwargs['phases__initial'] = [
            {'phase_content': phase,
             'type': phase.identifier,
             'weight': index
             } for index, phase in enumerate(blueprint.content)
        ]

        self.organisation = organisation
        self.blueprint = blueprint
        self.blueprint_key = blueprint_key
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

        self.show_categories_form = \
            self._show_categories_form(self.blueprint.content)
        if self.show_categories_form:
            # no initial categories in are shown in create view
            kwargs['categories__queryset'] = \
                category_models.Category.objects.none()
            self.base_forms.append(
                ('categories', dynamic_modelformset_factory(
                    category_models.Category, CategoryForm,
                    can_delete=True,
                ))
            )

        return super().__init__(*args, **kwargs)

    def save(self, commit=True):
        objects = super().save(commit=False)

        project = objects['project']
        project.organisation = self.organisation
        project.typ = self.blueprint_key
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
        for phase in phases:
            phase.module = module
            if commit:
                phase.save()

        if self.show_categories_form:
            categories = objects['categories']
            for category in categories:
                category.module = module
                if commit:
                    category.save()


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

        phases = [phase.content() for phase in qs]
        self.show_categories_form = self._show_categories_form(phases)
        if self.show_categories_form:
            self.base_forms.append(
                ('categories', dynamic_modelformset_factory(
                    category_models.Category, CategoryForm,
                    can_delete=True,
                ))
            )
        else:
            del kwargs['categories__queryset']

        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        objects = super().save(commit=False)
        project = objects['project']

        if commit:
            project.save()
            phases = objects['phases']
            for phase in phases:
                phase.save()
            if 'module_settings' in objects:
                objects['module_settings'].save()

        if self.show_categories_form:
            module = project.module_set.first()
            categories = objects['categories']
            for category in categories:
                category.module = module
                if commit:
                    category.save()
            for category in self.forms['categories'].deleted_objects:
                category.delete()


class OrganisationForm(forms.ModelForm):

    class Meta:
        model = Organisation
        fields = ['name', 'logo']
        labels = {
            'name': _('Organisation name')
        }


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


class ExternalProjectBaseForm(forms.ModelForm):

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

    def clean_end_date(self, *args, **kwargs):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        if start_date and end_date and end_date < start_date:
            raise ValidationError(
                _('End date can not be smaller than the start date.'))
        return end_date

    class Meta:
        model = extproject_models.ExternalProject
        fields = ['name', 'url', 'description', 'tile_image', 'is_archived']


class ExternalProjectCreateForm(ExternalProjectBaseForm):

    def __init__(self, organisation, creator, blueprint, blueprint_key,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.organisation = organisation
        self.creator = creator
        self.blueprint = blueprint
        self.blueprint_key = blueprint_key

    def save(self, commit=True):
        project = self.instance
        project.information = _('External projects require no information.')
        project.organisation = self.organisation
        project.typ = self.blueprint_key
        project = super().save(commit)

        if commit:
            project.moderators.add(self.creator)

        module = module_models.Module(
            name=project.slug + '_module',
            weight=1,
            project=project,
        )
        if commit:
            module.save()

        phase_content = extproject_phases.ExternalPhase()
        phase = phase_models.Phase(
            name=_('External project phase'),
            description=_('External project phase'),
            type=phase_content.identifier,
            module=module,
            start_date=self.cleaned_data['start_date'],
            end_date=self.cleaned_data['end_date']
        )
        if commit:
            phase.save()


class ExternalProjectUpdateForm(ExternalProjectBaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initial['start_date'] = self.instance.phase.start_date
        self.initial['end_date'] = self.instance.phase.end_date

    def save(self, commit=True):
        project = super().save(commit)

        if commit:
            phase = project.phase
            phase.start_date = self.cleaned_data['start_date']
            phase.end_date = self.cleaned_data['end_date']
            phase.save()


class BplanProjectBaseForm(ExternalProjectBaseForm):

    class Meta:
        model = bplan_models.Bplan
        fields = ['name', 'url', 'description', 'tile_image', 'is_archived',
                  'office_worker_email']


class BplanProjectCreateForm(BplanProjectBaseForm):

    def __init__(self, organisation, creator, blueprint, blueprint_key,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.organisation = organisation
        self.creator = creator
        self.blueprint = blueprint
        self.blueprint_key = blueprint_key

    def save(self, commit=True):
        project = self.instance
        project.information = _('Bplan projects require no information.')
        project.organisation = self.organisation
        project.typ = self.blueprint_key
        project = super().save(commit)

        if commit:
            project.moderators.add(self.creator)

        module = module_models.Module(
            name=project.slug + '_module',
            weight=1,
            project=project,
        )
        if commit:
            module.save()

        phase_content = bplan_phases.StatementPhase()
        phase = phase_models.Phase(
            name=_('Bplan statement phase'),
            description=_('Bplan statement phase'),
            type=phase_content.identifier,
            module=module,
            start_date=self.cleaned_data['start_date'],
            end_date=self.cleaned_data['end_date']
        )
        if commit:
            phase.save()


class BplanProjectUpdateForm(BplanProjectBaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initial['start_date'] = self.instance.phase.start_date
        self.initial['end_date'] = self.instance.phase.end_date

    def save(self, commit=True):
        project = super().save(commit)

        if commit:
            phase = project.phase
            phase.start_date = self.cleaned_data['start_date']
            phase.end_date = self.cleaned_data['end_date']
            phase.save()
