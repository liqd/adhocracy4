from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import ProjectFormComponent
from adhocracy4.dashboard import components

from . import forms
from . import views


class BplanProjectComponent(ProjectFormComponent):
    identifier = "bplan"
    weight = 10
    label = _("Development plan settings")

    form_title = _("Edit basic settings")
    form_class = forms.BplanProjectForm
    form_template_name = "meinberlin_bplan/includes" "/bplan_project_form.html"

    def is_effective(self, project):
        return project.project_type == "meinberlin_bplan.Bplan"

    def get_base_url(self, project):
        return reverse(
            "a4dashboard:dashboard-bplan-project-edit",
            kwargs={"project_slug": project.slug},
        )

    def get_urls(self):
        return [
            (
                r"^projects/(?P<project_slug>[-\w_]+)/bplan/$",
                views.BplanProjectUpdateView.as_view(
                    component=self,
                    title=self.form_title,
                    form_class=self.form_class,
                    form_template_name=self.form_template_name,
                ),
                "dashboard-bplan-project-edit",
            )
        ]

    def get_progress(self, project):
        project = project.externalproject.bplan

        num_valid, num_required = super().get_progress(project)
        phase_num_valid, phase_num_required = self._get_progress_for_object(
            project.phase, ["start_date", "end_date"]
        )

        return num_valid + phase_num_valid, num_required + phase_num_required


components.register_project(BplanProjectComponent())
