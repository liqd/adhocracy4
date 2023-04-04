from django_filters import rest_framework as rest_filters
from rest_framework.filters import OrderingFilter


class DistinctOrderingFilter(OrderingFilter):

    """Makes sure, that every queryset gets a distinct ordering.

    Even if field to order by (e.g. comment count) would produce a non-distinct
    ordering. The attr used for the distinct ordering can be set by
    distinct_ordering='attr' in the respective view, if it is not set,
    the default is 'pk'.
    """

    def get_ordering(self, request, queryset, view):
        distinct_ordering = getattr(view, "distinct_ordering", "pk")
        ordering = super().get_ordering(request, queryset, view)
        ordering += [distinct_ordering]
        return ordering


class DefaultsRestFilterSet(rest_filters.FilterSet):
    """Extend to define default filter values.
    Set the defaults attribute. E.g.:
        defaults = {
            'is_archived': 'false'
        }
    """

    defaults = None

    def __init__(self, data, *args, **kwargs):
        data = data.copy()

        # Set the defaults if they are not manually set yet
        for key, value in self.defaults.items():
            if key not in data:
                data[key] = value
        super().__init__(data, *args, **kwargs)
