import datetime

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms import RadioSelect
from django.forms import inlineformset_factory
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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


def _coerce_bool_choice(value):
    if isinstance(value, bool):
        return value
    if value in ("True", "true", "1", 1):
        return True
    if value in ("False", "false", "0", 0):
        return False
    raise ValueError(f"Invalid boolean choice: {value!r}")


ALLOW_GUEST_USERS_CHOICES = (
    (
        False,
        _("Only registered users can participate"),
    ),
    (
        True,
        _("Registered and guest users can participate"),
    ),
)


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = project_models.Project
        fields = ["name", "description", "image", "image_alt_text", "image_copyright"]

    def __init__(self, organisation, creator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.organisation = organisation
        self.creator = creator

    def save(self, commit=True):
        creator = self.creator
        org = self.organisation

        org_has_groups = hasattr(org, "groups")
        creator_has_groups = hasattr(creator, "groups")

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
            if hasattr(self, "save_m2m"):
                self.save_m2m()

        return project


class ProjectBasicForm(ProjectDashboardForm):
    class Meta:
        model = project_models.Project
        fields = [
            "name",
            "description",
            "image",
            "image_alt_text",
            "image_copyright",
            "tile_image",
            "tile_image_alt_text",
            "tile_image_copyright",
            "is_archived",
            "allow_guest_users",
            "access",
        ]
        required_for_project_publish = ["name", "description", "allow_guest_users"]
        widgets = {
            "access": RadioSelect(
                choices=[
                    (Access.PUBLIC, _("All users can participate (public).")),
                    (
                        Access.PRIVATE,
                        _("Only invited users can participate (private)."),
                    ),
                ]
            ),
        }

    @classmethod
    def get_required_fields(cls):
        required = super().get_required_fields()
        if not getattr(settings, "A4_ENABLE_GUEST_USERS", False):
            return [field for field in required if field != "allow_guest_users"]
        return required

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not getattr(settings, "A4_ENABLE_GUEST_USERS", False):
            self.fields.pop("allow_guest_users", None)
        else:
            self.fields["allow_guest_users"] = forms.TypedChoiceField(
                label=_("Participants"),
                choices=ALLOW_GUEST_USERS_CHOICES,
                coerce=_coerce_bool_choice,
                widget=RadioSelect(),
            )


class ProjectInformationForm(ProjectDashboardForm):
    contact_heading = _("Contact for questions")
    contact_help = _(
        "Please name a contact person. The user will "
        "then know who is carrying out this project and "
        "to whom they can address possible questions. "
        "The contact person will be shown in the "
        "information tab on the project page."
    )
    contact_info_label = _("More contact possibilities")

    class Meta:
        model = project_models.Project
        fields = [
            "information",
            "contact_name",
            "contact_address_text",
            "contact_phone",
            "contact_email",
            "contact_url",
        ]
        required_for_project_publish = ["information"]
        help_texts = {
            "information": _(
                "The project description will be shown in the info-tab. "
                "If you add an image, please provide an alternate text. "
                "It serves as a textual description of the image content and is "
                "read out by screen readers. Describe the image in approx. 80 "
                "characters. Example: A busy square with people in summer."
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["contact_address_text"].widget.attrs["rows"] = 6


class ProjectResultForm(ProjectDashboardForm):
    class Meta:
        model = project_models.Project
        fields = ["result"]
        required_for_project_publish = []
        help_texts = {
            "result": _(
                "The results description will be shown in the result-tab. "
                "Please describe a participation promise beforehand "
                "(what will happen with the outcome?) and inform afterwards "
                "about the outcome. If you add an image, please provide "
                "an alternate text. It serves as a textual description "
                "of the image content and is read out by screen readers. "
                "Describe the image in approx. 80 characters. "
                "Example: A busy square with people in summer."
            )
        }


class ModuleBasicForm(ModuleDashboardForm):
    class Meta:
        model = module_models.Module
        fields = ["name", "description"]
        required_for_project_publish = "__all__"

        widgets = {
            "description": forms.Textarea,
        }


class PhaseForm(forms.ModelForm):
    end_date = DateTimeField(
        time_format="%H:%M",
        time_default=datetime.time(
            hour=23, minute=59, tzinfo=timezone.get_default_timezone()
        ),
        required=False,
        require_all_fields=False,
        label=(_("End date"), _("End time")),
    )
    start_date = DateTimeField(
        time_format="%H:%M",
        required=False,
        require_all_fields=False,
        label=(_("Start date"), _("Start time")),
    )

    class Meta:
        model = phase_models.Phase
        fields = [
            "name",
            "description",
            "start_date",
            "end_date",
            "type",  # required for get_phase_name in the tpl
        ]
        required_for_project_publish = ["name", "description", "start_date", "end_date"]
        widgets = {"type": forms.HiddenInput(), "weight": forms.HiddenInput()}


class DashboardPhaseInlineFormSet(ModuleDashboardFormSet, PhaseInlineFormSet):
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
        self.module = kwargs["instance"]
        kwargs["instance"] = self.module.settings_instance
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        super().save(commit)
        return self.module

    def get_project(self):
        return self.module.project

    class Meta:
        model = map_models.AreaSettings
        fields = ["polygon"]
        required_for_project_publish = ["polygon"]
        widgets = map_models.AreaSettings.widgets()
