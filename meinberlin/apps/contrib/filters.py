import random
from datetime import date

from django.db.models import Case
from django.db.models import When
from django_filters import rest_framework as rest_filters
from rest_framework.filters import OrderingFilter


class OrderingFilterWithDailyRandom(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            if ordering == ["dailyrandom"]:
                pks = list(queryset.values_list("pk", flat=True))
                random.seed(str(date.today()))
                random.shuffle(pks)
                preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pks)])
                ordered_queryset = queryset.filter(pk__in=pks).order_by(preserved)
                return ordered_queryset
            else:
                return queryset.order_by(*ordering)

        return queryset


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
