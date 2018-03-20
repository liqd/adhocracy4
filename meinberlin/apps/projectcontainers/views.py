from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.dashboard import mixins as dashboard_mixins
from adhocracy4.dashboard.blueprints import ProjectBlueprint
from adhocracy4.dashboard.components.forms.views import \
    ProjectComponentFormView
from adhocracy4.dashboard.views import ProjectCreateView

from . import forms
from . import models


class ContainerCreateView(ProjectCreateView):
    model = models.ProjectContainer
    slug_url_kwarg = 'project_slug'
    form_class = forms.ContainerCreateForm
    template_name = 'meinberlin_projectcontainers/container_create_form.html'
    success_message = _('Container successfully created.')

    blueprint = ProjectBlueprint(
        title=_('Container'),
        description=_(
            'A container contains multiple projects.'
        ),
        content=[],
        image='',
        settings_model=None,
    )


class ContainerBasicFormView(ProjectComponentFormView):
    model = models.ProjectContainer

    @property
    def project(self):
        project = super().project
        return project.projectcontainer

    def get_object(self, queryset=None):
        return self.project


class ContainerProjectsView(ProjectComponentFormView):
    model = models.ProjectContainer

    @property
    def project(self):
        project = super().project
        return project.projectcontainer

    def get_object(self, queryset=None):
        return self.project


class ContainerListView(dashboard_mixins.DashboardBaseMixin,
                        generic.ListView):
    model = models.ProjectContainer
    paginate_by = 12
    template_name = 'meinberlin_projectcontainers/container_list.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'

    def get_queryset(self):
        return super().get_queryset().filter(
            organisation=self.organisation
        )

    def get_permission_object(self):
        return self.organisation
