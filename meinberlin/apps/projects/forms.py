from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard.forms import ProjectDashboardForm
from adhocracy4.maps import widgets as maps_widgets
from adhocracy4.projects.models import Project
from adhocracy4.projects.models import Topic
from meinberlin.apps.contrib.widgets import Select2Widget
from meinberlin.apps.users import fields as user_fields

from .models import ModeratorInvite
from .models import ParticipantInvite

User = get_user_model()


class InviteForm(forms.ModelForm):
    accept = forms.CharField(required=False)
    reject = forms.CharField(required=False)

    def clean(self):
        data = self.data
        if "accept" not in data and "reject" not in data:
            raise ValidationError("Reject or accept")
        return data

    def is_accepted(self):
        data = self.data
        return "accept" in data and "reject" not in data


class ParticipantInviteForm(InviteForm):
    class Meta:
        model = ParticipantInvite
        fields = ["accept", "reject"]


class ModeratorInviteForm(InviteForm):
    class Meta:
        model = ModeratorInvite
        fields = ["accept", "reject"]


class InviteUsersFromEmailForm(forms.Form):
    add_users = user_fields.CommaSeparatedEmailField(
        required=False, label=_("Invite users via email")
    )

    add_users_upload = user_fields.EmailFileField(
        required=False,
        label=_("Invite users via file upload"),
        help_text=_("Upload a csv file containing email addresses."),
    )

    def __init__(self, *args, **kwargs):
        labels = kwargs.pop("labels", None)
        super().__init__(*args, **kwargs)

        if labels:
            self.fields["add_users"].label = labels[0]
            self.fields["add_users_upload"].label = labels[1]

    def clean(self):
        cleaned_data = super().clean()
        add_users = self.data.get("add_users")
        add_users_upload = self.files.get("add_users_upload")
        if not self.errors and not add_users and not add_users_upload:
            raise ValidationError(_("Please enter email addresses or upload a file"))
        return cleaned_data


class TopicForm(ProjectDashboardForm):
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Project
        fields = ["topics"]
        required_for_project_publish = ["topics"]


class PointForm(ProjectDashboardForm):
    class Meta:
        model = Project
        fields = ["administrative_district", "point"]
        required_for_project_publish = []
        widgets = {
            "administrative_district": Select2Widget,
            "point": maps_widgets.MapChoosePointWidget(polygon=settings.BERLIN_POLYGON),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["administrative_district"].empty_label = _("City wide")
