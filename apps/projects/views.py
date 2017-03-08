import django_filters
from django.utils.translation import ugettext as _

from adhocracy4.contrib.views import FilteredListView
from adhocracy4.projects import models as project_models

from apps.contrib.widgets import DropdownLinkWidget


class OrderingWidget(DropdownLinkWidget):
    label = _('Ordering')
    right = True


class ProjectFilterSet(django_filters.FilterSet):

    ordering = django_filters.OrderingFilter(
        choices=(
            ('-created', _('Most recent')),
        ),
        empty_label=None,
        widget=OrderingWidget,
    )

    class Meta:
        model = project_models.Project
        fields = ['organisation']


class ProjectListView(FilteredListView):
    model = project_models.Project
    paginate_by = 16
    filter_set = ProjectFilterSet
