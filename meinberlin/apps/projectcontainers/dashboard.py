from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import ProjectFormComponent
from adhocracy4.dashboard import components

from . import forms
from . import views


class ContainerBasicComponent(ProjectFormComponent):
    identifier = 'container-basic'
    weight = 10
    label = _('Basic settings')

    form_title = _('Edit container settings')
    form_class = forms.ContainerBasicForm
    form_template_name = 'meinberlin_projectcontainers/includes' \
                         '/container_basic_form.html'

    def is_effective(self, project):
        return (project.project_type
                == 'meinberlin_projectcontainers.ProjectContainer')

    def get_base_url(self, project):
        return reverse('a4dashboard:dashboard-container-basic-edit', kwargs={
            'project_slug': project.slug
        })

    def get_urls(self):
        return [(
            r'^projects/(?P<project_slug>[-\w_]+)/container/$',
            views.ContainerBasicFormView.as_view(
                component=self,
                title=self.form_title,
                form_class=self.form_class,
                form_template_name=self.form_template_name
            ),
            'dashboard-container-basic-edit'
        )]


class ContainerInformationComponent(ProjectFormComponent):
    identifier = 'container-information'
    weight = 11
    label = _('Information')

    form_title = _('Edit project information')
    form_class = forms.ContainerInformationForm
    form_template_name = 'a4dashboard/includes/project_information_form.html'

    def is_effective(self, project):
        return (project.project_type
                == 'meinberlin_projectcontainers.ProjectContainer')


class ContainerProjectsComponent(ProjectFormComponent):
    identifier = 'container-projects'
    weight = 20
    label = _('Projects')

    form_title = _('Select projects')
    form_class = forms.ContainerProjectsForm
    form_template_name = 'meinberlin_projectcontainers/includes' \
                         '/container_projects_form.html'

    def is_effective(self, project):
        return (project.project_type
                == 'meinberlin_projectcontainers.ProjectContainer')

    def get_base_url(self, project):
        return reverse('a4dashboard:dashboard-container-projects', kwargs={
            'project_slug': project.slug
        })

    def get_urls(self):
        return [(
            r'^projects/(?P<project_slug>[-\w_]+)/container-projects/$',
            views.ContainerProjectsView.as_view(
                component=self,
                title=self.form_title,
                form_class=self.form_class,
                form_template_name=self.form_template_name
            ),
            'dashboard-container-projects'
        )]

    def get_progress(self, project):
        if project.projectcontainer.projects.all().exists():
            return 1, 1
        return 0, 1


components.register_project(ContainerBasicComponent())
components.register_project(ContainerInformationComponent())
components.register_project(ContainerProjectsComponent())
