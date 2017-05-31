from datetime import datetime
import django_filters
from django.apps import apps
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from adhocracy4.filters import views as filter_views
from adhocracy4.filters.filters import DefaultsFilterSet
from adhocracy4.projects import models as project_models

from apps.contrib.widgets import DropdownLinkWidget
from apps.dashboard import blueprints


class OrderingWidget(DropdownLinkWidget):
    label = _('Ordering')
    right = True


class OrganisationWidget(DropdownLinkWidget):
    label = _('Organisation')


class ArchivedWidget(DropdownLinkWidget):
    label = _('Archived')

    def __init__(self, attrs=None):
        choices = (
            ('', _('All')),
            ('false', _('No')),
            ('true', _('Yes')),
        )
        super().__init__(attrs, choices)


class YearWidget(DropdownLinkWidget):
    label = _('Year')

    def __init__(self, attrs=None):
        choices = (('', _('Any')),)
        now = datetime.now().year
        try:
            first_year = project_models.Project.objects.earliest('created').\
                created.year
        except project_models.Project.DoesNotExist:
            first_year = now
        for year in range(now, first_year - 1, -1):
            choices += (year, year),
        super().__init__(attrs, choices)


class TypeWidget(DropdownLinkWidget):
    label = _('Project Type')

    def __init__(self, attrs=None):
        choices = (('', _('Any')),)
        sorted_blueprints = sorted(blueprints.blueprints, key=lambda a: a[1])
        for blueprint_key, blueprint in sorted_blueprints:
            choices += (blueprint_key, blueprint.title),
        super().__init__(attrs, choices)


class ProjectFilterSet(DefaultsFilterSet):

    defaults = {
        'is_archived': 'false'
    }

    ordering = django_filters.OrderingFilter(
        choices=(
            ('-created', _('Most recent')),
        ),
        empty_label=None,
        widget=OrderingWidget,
    )

    organisation = django_filters.ModelChoiceFilter(
        queryset=apps.get_model(settings.A4_ORGANISATIONS_MODEL).objects
                     .order_by('name'),
        widget=OrganisationWidget,
    )

    is_archived = django_filters.BooleanFilter(
        widget=ArchivedWidget
    )

    created = django_filters.NumberFilter(
        name='created',
        lookup_expr='year',
        widget=YearWidget,
    )

    typ = django_filters.CharFilter(
        widget=TypeWidget,
    )

    class Meta:
        model = project_models.Project
        fields = ['organisation', 'is_archived', 'created', 'typ']


class ProjectListView(filter_views.FilteredListView):
    model = project_models.Project
    paginate_by = 16
    filter_set = ProjectFilterSet

    def get_queryset(self):
        return super().get_queryset().filter(is_draft=False)
