from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import ProjectFormComponent
from adhocracy4.dashboard import components

from . import forms
from . import views


class ExternalProjectComponent(ProjectFormComponent):
    identifier = "external"
    weight = 10
    label = _("External project settings")

    form_title = _("Edit basic settings")
    form_class = forms.ExternalProjectForm
    form_template_name = "meinberlin_extprojects/includes" "/external_project_form.html"

    def is_effective(self, project):
        return project.project_type == "meinberlin_extprojects.ExternalProject"

    def get_base_url(self, project):
        return reverse(
            "a4dashboard:dashboard-external-project-edit",
            kwargs={"project_slug": project.slug},
        )

    def get_urls(self):
        return [
            (
                r"^projects/(?P<project_slug>[-\w_]+)/external/$",
                views.ExternalProjectUpdateView.as_view(
                    component=self,
                    title=self.form_title,
                    form_class=self.form_class,
                    form_template_name=self.form_template_name,
                ),
                "dashboard-external-project-edit",
            )
        ]


components.register_project(ExternalProjectComponent())
