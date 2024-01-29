import pytest
from django import forms
from django.forms import inlineformset_factory
from django.utils.timezone import now

from adhocracy4.dashboard.components.forms import ModuleDashboardForm
from adhocracy4.dashboard.components.forms import ModuleDashboardFormSet
from adhocracy4.dashboard.components.forms import ModuleFormComponent
from adhocracy4.dashboard.components.forms import ModuleFormSetComponent
from adhocracy4.dashboard.components.forms import ProjectDashboardForm
from adhocracy4.dashboard.components.forms import ProjectFormComponent
from adhocracy4.dashboard.forms import ProjectBasicForm
from adhocracy4.dashboard.forms import ProjectInformationForm
from adhocracy4.dashboard.forms import ProjectResultForm
from adhocracy4.images.validators import ImageAltTextValidator
from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models
from adhocracy4.projects.enums import Access


@pytest.mark.django_db
def test_project_form_required_for_publish(project_factory):
    class Form(ProjectDashboardForm):
        class Meta:
            model = project_models.Project
            fields = ["information"]
            required_for_project_publish = ["information"]

    project = project_factory(is_draft=True)

    form = Form(instance=project)
    assert form.get_required_fields() == ["information"]
    assert form.fields["information"].required is False

    project.is_draft = False
    form = Form(instance=project)
    assert form.fields["information"].required is True


@pytest.mark.django_db
def test_project_form_for_publish_all_fields(project_factory):
    class Form(ProjectDashboardForm):
        class Meta:
            model = project_models.Project
            fields = ["information", "result"]
            required_for_project_publish = "__all__"

    project = project_factory(is_draft=False)

    form = Form(instance=project)
    assert form.get_required_fields() == "__all__"
    assert all(map(lambda field: field.required is True, form.fields.values()))


@pytest.mark.django_db
def test_project_form_component(project_factory):
    class Form(ProjectDashboardForm):
        class Meta:
            model = project_models.Project
            fields = ["information", "result"]
            required_for_project_publish = ["information"]

    class Component(ProjectFormComponent):
        identifier = "test_id"
        weight = 1
        label = "Project Settings"

        form_title = "Edit test project settings"
        form_class = Form
        form_template_name = "none"

    project = project_factory(information="", result="")

    component = Component()
    assert component.is_effective(project) is True

    urls = component.get_urls()
    assert len(urls) == 1
    regexp, _, name = urls[0]
    assert regexp == r"^projects/(?P<project_slug>[-\w_]+)/test_id/$"
    assert name == "dashboard-test_id-edit"

    assert component.get_progress(project) == (0, 1)

    project.information = "some information"
    assert component.get_progress(project) == (1, 1)


@pytest.mark.django_db
def test_project_basic_form_image_metadata_mixin(project_factory, image_factory):
    image = image_factory((1440, 1400))
    project = project_factory(is_draft=False, image=image)
    project_form = ProjectBasicForm(
        instance=project,
        data={
            "name": "my project",
            "description": "my project description",
            "access": Access.PUBLIC.value,
        },
    )
    assert not project_form.is_valid()
    assert "image_copyright" in project_form.errors
    assert "image_alt_text" in project_form.errors

    project_form = ProjectBasicForm(
        instance=project,
        data={
            "name": "my project",
            "description": "my project description",
            "access": Access.PUBLIC.value,
            "image_copyright": "my copyright",
            "image_alt_text": "my alt text",
        },
    )
    assert project_form.is_valid()


@pytest.mark.django_db
def test_module_form_required_for_publish(module_factory):
    class Form(ModuleDashboardForm):
        class Meta:
            model = module_models.Module
            fields = ["description"]
            required_for_project_publish = ["description"]

    module = module_factory(project__is_draft=True)
    project = module.project

    form = Form(instance=module)
    assert form.get_required_fields() == ["description"]
    assert form.fields["description"].required is False

    project.is_draft = False
    form = Form(instance=module)
    assert form.fields["description"].required is True


@pytest.mark.django_db
def test_module_form_required_for_publish_all(module_factory):
    class Form(ModuleDashboardForm):
        class Meta:
            model = module_models.Module
            fields = ["description", "name"]
            required_for_project_publish = "__all__"

    module = module_factory(project__is_draft=False)

    form = Form(instance=module)
    assert form.get_required_fields() == "__all__"
    assert all(map(lambda field: field.required is True, form.fields.values()))


@pytest.mark.django_db
def test_module_form_component(module_factory):
    class Form(ProjectDashboardForm):
        class Meta:
            model = module_models.Module
            fields = ["description"]
            required_for_project_publish = ["description"]

    class Component(ModuleFormComponent):
        identifier = "test_id"
        weight = 1
        label = "Module Settings"

        form_title = "Edit test module settings"
        form_class = Form
        form_template_name = "none"

    module = module_factory(description="")

    component = Component()
    assert component.is_effective(module) is True

    urls = component.get_urls()
    assert len(urls) == 1
    regexp, _, name = urls[0]
    assert regexp == r"^modules/(?P<module_slug>[-\w_]+)/test_id/$"
    assert name == "dashboard-test_id-edit"

    assert component.get_progress(module) == (0, 1)

    module.description = "some information"
    assert component.get_progress(module) == (1, 1)


@pytest.mark.django_db
def test_module_formset_required_for_publish(phase_factory):
    class Form(forms.ModelForm):
        class Meta:
            model = phase_models.Phase
            fields = ["start_date"]
            required_for_project_publish = ["start_date"]
            widgets = {"start_date": forms.TextInput()}

    FormSet = inlineformset_factory(
        module_models.Module,
        phase_models.Phase,
        form=Form,
        formset=ModuleDashboardFormSet,
        extra=0,
        can_delete=False,
    )

    phase = phase_factory(module__project__is_draft=True)
    module = phase.module
    project = module.project
    phase_factory(module=module)

    formset = FormSet(instance=module)
    assert formset.get_required_fields() == ["start_date"]
    assert all(
        map(
            lambda field: field.required is False,
            [form.fields["start_date"] for form in formset.forms],
        )
    )

    project.is_draft = False
    formset = FormSet(instance=module)
    assert formset.get_required_fields() == ["start_date"]
    assert all(
        map(
            lambda field: field.required is True,
            [form.fields["start_date"] for form in formset.forms],
        )
    )


@pytest.mark.django_db
def test_module_formset_component(phase_factory):
    class Form(forms.ModelForm):
        class Meta:
            model = phase_models.Phase
            fields = ["start_date"]
            required_for_project_publish = ["start_date"]
            widgets = {"start_date": forms.TextInput()}

    FormSet = inlineformset_factory(
        module_models.Module,
        phase_models.Phase,
        form=Form,
        formset=ModuleDashboardFormSet,
        extra=0,
        can_delete=False,
    )

    class Component(ModuleFormSetComponent):
        identifier = "test_id"
        weight = 1
        label = "Module Settings"

        form_title = "Edit test module settings"
        form_class = FormSet
        form_template_name = "none"

    phase = phase_factory(module__project__is_draft=True, start_date=None)
    module = phase.module
    phase_factory(module=module, start_date=None)

    component = Component()
    assert component.is_effective(module) is True

    urls = component.get_urls()
    assert len(urls) == 1
    regexp, _, name = urls[0]
    assert regexp == r"^modules/(?P<module_slug>[-\w_]+)/test_id/$"
    assert name == "dashboard-test_id-edit"

    assert component.get_progress(module) == (0, 2)

    phase.start_date = now()
    phase.save()
    assert component.get_progress(module) == (1, 2)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "form_class, field_name",
    [(ProjectInformationForm, "information"), (ProjectResultForm, "result")],
)
def test_project_form_image_missing_alt_text(form_class, field_name, project_factory):
    project = project_factory(is_draft=False)
    form = form_class(
        instance=project,
        data={
            field_name: "my project description <img>",
        },
    )
    assert field_name in form.errors
    assert form.errors[field_name].data[0].messages[0] == ImageAltTextValidator.message
    assert not form.is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "form_class, field_name",
    [(ProjectInformationForm, "information"), (ProjectResultForm, "result")],
)
def test_project_form_image_has_alt_text(form_class, field_name, project_factory):
    project = project_factory(is_draft=False)
    form = form_class(
        instance=project,
        data={
            field_name: "my project description <img alt='descriptive picture'>",
        },
    )
    assert field_name not in form.errors
    assert form.is_valid()
