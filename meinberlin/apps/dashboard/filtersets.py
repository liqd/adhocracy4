import django_filters
from django.utils.translation import ugettext_lazy as _

from adhocracy4.filters import widgets as filters_widgets
from adhocracy4.filters.filters import DefaultsFilterSet
from adhocracy4.filters.filters import FreeTextFilter
from adhocracy4.projects.models import Project
from meinberlin.apps.projects import views


class FreeTextFilterWidget(filters_widgets.FreeTextFilterWidget):
    label = _('Search')


class DashboardProjectFilterSet(DefaultsFilterSet):

    defaults = {
        'is_archived': 'false'
    }

    ordering = django_filters.OrderingFilter(
        choices=(
            ('-created', _('Most recent')),
        ),
        empty_label=None,
        widget=views.OrderingWidget,
    )

    search = FreeTextFilter(
        widget=FreeTextFilterWidget,
        fields=['name']
    )

    is_archived = django_filters.BooleanFilter(
        widget=views.ArchivedWidget
    )

    created = django_filters.NumberFilter(
        name='created',
        lookup_expr='year',
        widget=views.YearWidget,
    )

    class Meta:
        model = Project
        fields = ['search', 'is_archived', 'created']
