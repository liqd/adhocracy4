from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard.forms import ProjectCreateForm
from adhocracy4.dashboard.forms import ProjectDashboardForm
from adhocracy4.forms.fields import DateTimeField
from meinberlin.apps.extprojects import models as extproject_models


class ExternalProjectCreateForm(ProjectCreateForm):
    class Meta:
        model = extproject_models.ExternalProject
        fields = [
            "name",
            "description",
            "tile_image",
            "tile_image_alt_text",
            "tile_image_copyright",
        ]


class ExternalProjectForm(ProjectDashboardForm):
    start_date = DateTimeField(
        time_format="%H:%M",
        required=False,
        require_all_fields=False,
        label=(_("Start date"), _("Start time")),
    )
    end_date = DateTimeField(
        time_format="%H:%M",
        required=False,
        require_all_fields=False,
        label=(_("End date"), _("End time")),
    )

    class Meta:
        model = extproject_models.ExternalProject
        fields = [
            "name",
            "url",
            "description",
            "tile_image",
            "tile_image_alt_text",
            "tile_image_copyright",
            "is_archived",
            "start_date",
            "end_date",
        ]
        required_for_project_publish = [
            "name",
            "url",
            "description",
            "start_date",
            "end_date",
        ]

    def clean_end_date(self, *args, **kwargs):
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")

        if start_date and not end_date or not start_date and end_date:
            raise ValidationError(
                _(
                    "Either both start and end date have to be provided "
                    "or none of them."
                )
            )

        if start_date and end_date and end_date < start_date:
            raise ValidationError(_("End date can not be smaller than the start date."))
        return end_date

    def save(self, commit=True):
        project = super().save(commit)

        if commit:
            phase = project.phase
            phase.start_date = self.cleaned_data["start_date"]
            phase.end_date = self.cleaned_data["end_date"]
            phase.save()
