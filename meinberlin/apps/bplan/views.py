from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from adhocracy4.dashboard.blueprints import ProjectBlueprint
from adhocracy4.dashboard.components.forms.views import \
    ProjectComponentFormView
from adhocracy4.dashboard.mixins import DashboardBaseMixin
from adhocracy4.filters import views as filter_views
from adhocracy4.filters import widgets as filter_widgets
from adhocracy4.filters.filters import DefaultsFilterSet
from adhocracy4.filters.filters import FreeTextFilter
from meinberlin.apps.bplan import phases as bplan_phases
from meinberlin.apps.dashboard.mixins import DashboardProjectListGroupMixin
from meinberlin.apps.extprojects.views import ExternalProjectCreateView

from . import forms
from . import models


class FreeTextFilterWidget(filter_widgets.FreeTextFilterWidget):
    label = _('Search')


class BPlanFilterSet(DefaultsFilterSet):
    defaults = {}

    search = FreeTextFilter(
        widget=FreeTextFilterWidget,
        fields=['name']
    )

    class Meta:
        model = models.Bplan
        fields = ['search']


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
                           filter_views.FilteredListView):
    model = models.Bplan
    paginate_by = 12
    template_name = 'meinberlin_bplan/bplan_list_dashboard.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'
    filter_set = BPlanFilterSet

    def get_queryset(self):
        return super().get_queryset().filter(
            organisation=self.organisation
        )

    def get_permission_object(self):
        return self.organisation
