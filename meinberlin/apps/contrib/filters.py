from rest_framework.filters import BaseFilterBackend


class IdeaCategoryFilterBackend(BaseFilterBackend):
    """Filter ideas for the categories in API."""

    def filter_queryset(self, request, queryset, view):

        if 'category' in request.GET:
            category = request.GET['category']
            return queryset.filter(category=category)

        return queryset
