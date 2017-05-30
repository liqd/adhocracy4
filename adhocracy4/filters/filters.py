import django_filters


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
