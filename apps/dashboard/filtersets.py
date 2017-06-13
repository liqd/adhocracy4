import django_filters
from django.utils.translation import ugettext_lazy as _

from adhocracy4.filters.filters import DefaultsFilterSet
from adhocracy4.projects.models import Project
from apps.projects import views


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

    is_archived = django_filters.BooleanFilter(
        widget=views.ArchivedWidget
    )

    created = django_filters.NumberFilter(
        name='created',
        lookup_expr='year',
        widget=views.YearWidget,
    )

    typ = django_filters.CharFilter(
        widget=views.TypeWidget,
    )

    class Meta:
        model = Project
        fields = ['is_archived', 'created', 'typ']
