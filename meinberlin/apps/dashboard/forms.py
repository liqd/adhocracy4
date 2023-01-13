from django import forms
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard.forms import ProjectCreateForm
from adhocracy4.projects import models as project_models
from meinberlin.apps.organisations.models import Organisation


class OrganisationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["address"].required = True
        self.fields["url"].required = True
        self.fields["url"].help_text = _(
            "Please enter " "a full url which " "starts with https:// " "or http://"
        )

    class Meta:
        model = Organisation
        fields = ["name", "logo", "address", "url"]
        labels = {"name": _("Organisation name")}


class DashboardProjectCreateForm(ProjectCreateForm):
    class Meta:
        model = project_models.Project
        fields = ["name", "description", "access"]
        widgets = {
            "access": forms.RadioSelect(
                # FIXME: these choices are currently ignored by djangos widget
                # machinery - we work around that in apps/projects/overwrites
                choices=[
                    (
                        project_models.Access.PUBLIC.value,
                        _(
                            "All users can see project tile and content and can "
                            "participate (public)."
                        ),
                    ),
                    (
                        project_models.Access.SEMIPUBLIC.value,
                        _(
                            "All users can see project tile and content, only "
                            "invited users can participate (semi-public)."
                        ),
                    ),
                    (
                        project_models.Access.PRIVATE.value,
                        _(
                            "Only invited users can see project tile and content "
                            "and can participate (private)."
                        ),
                    ),
                ]
            )
        }
