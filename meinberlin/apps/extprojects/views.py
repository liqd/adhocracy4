from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard.blueprints import ProjectBlueprint
from adhocracy4.dashboard.components.forms.views import \
    ProjectComponentFormView
from adhocracy4.dashboard.mixins import DashboardBaseMixin
from adhocracy4.dashboard.views import ProjectCreateView
from adhocracy4.filters import views as filter_views
from adhocracy4.filters import widgets as filter_widgets
from adhocracy4.filters.filters import DefaultsFilterSet
from adhocracy4.filters.filters import FreeTextFilter
from meinberlin.apps.dashboard.mixins import DashboardProjectListGroupMixin
from meinberlin.apps.extprojects import phases as extprojects_phases

from . import apps
from . import forms
from . import models


class FreeTextFilterWidget(filter_widgets.FreeTextFilterWidget):
    label = _('Search')


class ExternalProjectFilterSet(DefaultsFilterSet):
    defaults = {}

    search = FreeTextFilter(
        widget=FreeTextFilterWidget,
        fields=['name']
    )

    class Meta:
        model = models.ExternalProject
        fields = ['search']


class ExternalProjectCreateView(ProjectCreateView):

    model = models.ExternalProject
    slug_url_kwarg = 'project_slug'
    form_class = forms.ExternalProjectCreateForm
    template_name = \
        'meinberlin_extprojects/external_project_create_dashboard.html'
    success_message = _('Project was created.')

    blueprint = ProjectBlueprint(
        title=_('Linkage'),
        description=_(
            'Linkages are handled on a different platform.'
        ),
        content=[
            extprojects_phases.ExternalPhase(),
        ],
        image='',
        settings_model=None,
        type='EP',
    )


class ExternalProjectUpdateView(ProjectComponentFormView):

    model = models.ExternalProject

    @property
    def project(self):
        project = super().project
        return project.externalproject

    def get_object(self, queryset=None):
        return self.project


class ExternalProjectListView(DashboardProjectListGroupMixin,
                              DashboardBaseMixin,
                              filter_views.FilteredListView):
    model = models.ExternalProject
    paginate_by = 12
    template_name = 'meinberlin_extprojects/extproject_list_dashboard.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'
    filter_set = ExternalProjectFilterSet

    def get_queryset(self):
        project_type = '{}.{}'.format(
            apps.Config.label,
            'ExternalProject'
        )
        return super().get_queryset().filter(
            organisation=self.organisation,
            project_type=project_type
        )

    def get_permission_object(self):
        return self.organisation
