from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.views.generic import TemplateView

from adhocracy4.dashboard.blueprints import ProjectBlueprint
from adhocracy4.dashboard.components.forms.views import \
    ProjectComponentFormView
from adhocracy4.dashboard.mixins import DashboardBaseMixin
from meinberlin.apps.bplan import phases as bplan_phases
from meinberlin.apps.dashboard.mixins import DashboardProjectListGroupMixin
from meinberlin.apps.extprojects.views import ExternalProjectCreateView

from . import forms
from . import models


class BplanStatementSentView(TemplateView):
    template_name = 'meinberlin_bplan/statement_sent.html'


class BplanFinishedView(TemplateView):
    template_name = 'meinberlin_bplan/bplan_finished.html'


class BplanProjectCreateView(ExternalProjectCreateView):

    model = models.Bplan
    slug_url_kwarg = 'project_slug'
    form_class = forms.BplanProjectCreateForm
    template_name = \
        'meinberlin_bplan/bplan_create_dashboard.html'
    success_message = _('Project was created.')

    blueprint = ProjectBlueprint(
        title=_('Development Plan'),
        description=_('Create a statement formular for development plans'
                      ' to be embedded on external sites.'),
        content=[
            bplan_phases.StatementPhase(),
        ],
        image='',
        settings_model=None,
    )


class BplanProjectUpdateView(ProjectComponentFormView):

    model = models.Bplan

    @property
    def project(self):
        project = super().project
        return project.externalproject.bplan

    def get_object(self, queryset=None):
        return self.project


class BplanProjectListView(DashboardProjectListGroupMixin,
                           DashboardBaseMixin,
                           generic.ListView):
    model = models.Bplan
    paginate_by = 12
    template_name = 'meinberlin_bplan/bplan_list_dashboard.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'

    def get_queryset(self):
        return super().get_queryset().filter(
            organisation=self.organisation
        )

    def get_permission_object(self):
        return self.organisation
