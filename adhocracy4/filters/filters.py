import django_filters
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from functools import reduce
import operator


class PagedFilterSet(django_filters.FilterSet):
    """Removes page parameters from the query when applying filters."""

    page_kwarg = 'page'

    def __init__(self, data, *args, **kwargs):
        if self.page_kwarg in data:
            # Create a mutable copy
            data = data.copy()
            del data[self.page_kwarg]
        return super().__init__(data=data, *args, **kwargs)


class DefaultsFilterSet(PagedFilterSet):
    """Extend to define default filter values.

    Set the defaults attribute. E.g.:
        defaults = {
            'is_archived': 'false'
        }
    """

    defaults = None

    def __init__(self, query_data, *args, **kwargs):
        data = query_data.copy()

        # Set the defaults if they are not manually set yet
        for key, value in self.defaults.items():
            if key not in data:
                data[key] = value

        super().__init__(data, *args, **kwargs)


class FreeTextFilter(django_filters.CharFilter):
    """Free text filter searches given fields.

    Set fields to search on.
    """

    def multi_filter(self, qs, name, value):
        if value:
            qs = qs.filter(reduce(operator.or_, self.get_q_objects(value)))
        return qs

    def get_q_objects(self, value):
        q_objects = [Q(((field + '__icontains'), value))
                     for field in self.fields]
        return q_objects

    def __init__(self, *args, **kwargs):
        kwargs['method'] = self.multi_filter

        if 'fields' in kwargs:
            self.fields = kwargs.pop('fields')
        else:
            raise ImproperlyConfigured('set fields to search on')

        super().__init__(*args, **kwargs)
