from django.views import generic

"""
Common views.

"""


class FilteredListView(generic.ListView):
    """List view with support for filtering and sorting via django-filter.

    Usage:
        Set filter_set to your django_filters.FilterSet definition.
        Use view.filter.form in the template to access the filter form.

    Note:
        Use the filter qs property instead of overriding get_queryset() to
        prefilter or annotate the basic queryset.
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
