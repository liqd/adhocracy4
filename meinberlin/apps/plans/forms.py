from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard.components.forms import ProjectDashboardForm
from adhocracy4.maps import widgets as maps_widgets
from adhocracy4.projects import models as project_models
from meinberlin.apps.contrib.widgets import Select2Widget

from . import models


class PlanForm(forms.ModelForm):
    class Meta:
        model = models.Plan
        fields = [
            "title",
            "description_image",
            "description_image_copyright",
            "point",
            "point_label",
            "district",
            "contact_name",
            "contact_address_text",
            "contact_phone",
            "contact_email",
            "contact_url",
            "cost",
            "description",
            "topics",
            "status",
            "participation",
            "participation_explanation",
            "duration",
            "tile_image",
            "tile_image_copyright",
        ]
        widgets = {
            "point": maps_widgets.MapChoosePointWidget(polygon=settings.BERLIN_POLYGON)
        }
        error_messages = {
            "point": {"required": _("Please locate the plan on the map.")}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["district"].empty_label = _("City wide")
        self.fields["contact_address_text"].widget.attrs["rows"] = 6
        self.fields["participation_explanation"].widget.attrs["rows"] = 1

    def save(self, commit=True):
        plan = super().save(commit=False)
        if not plan.group:
            group = plan._get_group(plan.creator, plan.organisation)
            plan.group = group
        if commit:
            plan.save()
        return plan


class CustomMultipleChoiceField(forms.ModelMultipleChoiceField):

    widget = forms.Select

    def clean(self, value):
        if not value:
            return super().clean([])
        return super().clean([value])


class ProjectPlansDashboardForm(ProjectDashboardForm):
    plans = CustomMultipleChoiceField(queryset=None, label=_("Plans"))

    class Meta:
        model = project_models.Project
        fields = ["plans"]
        required = False
        widgets = {
            "plans": Select2Widget,
        }

    def save(self, commit=False):
        plans = self.cleaned_data["plans"]
        self.instance.plans.set(plans)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial["plans"] = self.instance.plans.all()
        self.fields["plans"].required = False
        self.fields["plans"].empty_label = "----------"
        self.fields["plans"].queryset = self.instance.organisation.plan_set.all()
