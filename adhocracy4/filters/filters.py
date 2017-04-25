import django_filters
from django.http import QueryDict


class DefaultsFilterSet(django_filters.FilterSet):
    """Extend to define default filter values.

    Set the defaults attribute. E.g.:
        defaults = {
            'is_archived': 'false'
        }
    """

    defaults = None

    def __init__(self, query_data, *args, **kwargs):
        data = QueryDict(mutable=True)
        data.update(self.defaults)
        data.update(query_data)
        super().__init__(data, *args, **kwargs)
