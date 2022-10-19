import random
from datetime import date

from django.db.models import Case
from django.db.models import When
from rest_framework.filters import BaseFilterBackend
from rest_framework.filters import OrderingFilter


class IdeaCategoryFilterBackend(BaseFilterBackend):
    """Filter ideas for the categories in API."""

    def filter_queryset(self, request, queryset, view):

        if 'category' in request.GET:
            category = request.GET['category']
            return queryset.filter(category=category)

        return queryset


class OrderingFilterWithDailyRandom(OrderingFilter):

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            if ordering == ['dailyrandom']:
                pks = list(queryset.values_list('pk', flat=True))
                random.seed(str(date.today()))
                random.shuffle(pks)
                preserved = \
                    Case(*[When(pk=pk, then=pos)
                           for pos, pk in enumerate(pks)])
                ordered_queryset = queryset \
                    .filter(pk__in=pks) \
                    .order_by(preserved)
                return ordered_queryset
            else:
                return queryset.order_by(*ordering)

        return queryset
