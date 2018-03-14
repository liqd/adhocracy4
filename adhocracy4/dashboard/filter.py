import django_filters
from django.utils.translation import ugettext_lazy as _

from adhocracy4.filters import widgets as filters_widgets
from adhocracy4.filters.filters import DefaultsFilterSet
from adhocracy4.filters.filters import FreeTextFilter
from adhocracy4.projects.models import Project


class FreeTextFilterWidget(filters_widgets.FreeTextFilterWidget):
    label = _('Search')


class ArchivedWidget(filters_widgets.DropdownLinkWidget):
    label = _('Archived')

    def __init__(self, attrs=None):
        choices = (
            ('', _('All')),
            ('false', _('No')),
            ('true', _('Yes')),
        )
        super().__init__(attrs, choices)


class ProjectFilterSet(DefaultsFilterSet):

    defaults = {
        'is_archived': 'false'
    }

    search = FreeTextFilter(
        widget=FreeTextFilterWidget,
        fields=['name', 'description']
    )

    is_archived = django_filters.BooleanFilter(
        widget=ArchivedWidget
    )

    class Meta:
        model = Project
        fields = ['search', 'is_archived']
