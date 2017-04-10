from django.views import generic


class FilteredListView(generic.ListView):
    """List view with support for filtering and sorting via django-filter.

    Usage:
        Set filter_set to your django_filters.FilterSet definition.
        Use view.filter.form in the template to access the filter form.

    Note:
        Always call super().get_queryset() when customizing get_queryset() to
        include the filter functionality.
    """

    filter_set = None

    def filter(self):
        return self.filter_set(
            self.request.GET,
            request=self.request
        )

    def get_queryset(self):
        qs = self.filter().qs
        return qs
