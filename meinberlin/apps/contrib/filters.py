from django.utils.translation import gettext_lazy as _
from rest_framework.filters import BaseFilterBackend

from adhocracy4.filters.filters import DistinctOrderingFilter
from adhocracy4.filters.widgets import DropdownLinkWidget

from . import mixins


class OrderingWidget(DropdownLinkWidget):
    label = _('Ordering')
    right = True


class OrderingFilter(mixins.DynamicChoicesMixin,
                     DistinctOrderingFilter):

    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = OrderingWidget
        kwargs['empty_label'] = None
        super().__init__(*args, **kwargs)


class IdeaCategoryFilterBackend(BaseFilterBackend):
    """Filter ideas for the categories in API."""

    def filter_queryset(self, request, queryset, view):

        if 'category' in request.GET:
            category = request.GET['category']
            return queryset.filter(category=category)

        return queryset
