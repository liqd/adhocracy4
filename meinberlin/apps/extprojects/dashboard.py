from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from meinberlin.apps.dashboard import get_project_type
from meinberlin.apps.dashboard2 import ProjectFormComponent
from meinberlin.apps.dashboard2 import components

from . import forms
from . import views


class ExternalProjectComponent(ProjectFormComponent):
    identifier = 'external'
    weight = 10
    label = _('External project settings')

    form_title = _('Edit external project settings')
    form_class = forms.ExternalProjectForm
    form_template_name = 'meinberlin_extprojects/includes' \
                         '/external_project_form.html'

    def is_effective(self, project):
        project_type = get_project_type(project)
        return project_type == 'external'

    def get_base_url(self, project):
        return reverse('a4dashboard:dashboard-external-project-edit', kwargs={
            'project_slug': project.slug
        })

    def get_urls(self):
        return [(
            r'^projects/(?P<project_slug>[-\w_]+)/external/$',
            views.ExternalProjectUpdateView.as_view(
                component=self,
                title=self.form_title,
                form_class=self.form_class,
                form_template_name=self.form_template_name
            ),
            'dashboard-external-project-edit'
        )]

    def get_progress(self, project):
        project = project.externalproject

        num_valid, num_required = super().get_progress(project)
        phase_num_valid, phase_num_required = \
            self._get_progress_for_object(project.phase,
                                          ['start_date', 'end_date'])

        return num_valid + phase_num_valid, num_required + phase_num_required


components.register_project(ExternalProjectComponent())
