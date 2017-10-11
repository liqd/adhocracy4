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

    def filter_kwargs(self):
        default_kwargs = {
            'data': self.request.GET,
            'request': self.request,
            'queryset': super().get_queryset(),
        }

        if getattr(self.filter_set, 'class_based_filterset', False):
            default_kwargs['view'] = self

        return default_kwargs

    def filter(self):
        return self.filter_set(
            **self.filter_kwargs()
        )

    def get_queryset(self):
        qs = self.filter().qs
        return qs
