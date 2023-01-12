import operator
import random
from datetime import date
from functools import reduce

import django_filters
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Case
from django.db.models import Q
from django.db.models import When

from adhocracy4.filters.mixins import DynamicChoicesMixin
from adhocracy4.filters.widgets import OrderingWidget


class ClassBasedViewFilterSet(django_filters.FilterSet):
    """Passes the view instance through to the filters of the set."""

    class_based_filterset = True

    def __init__(self, *args, view, **kwargs):
        super().__init__(*args, **kwargs)
        self.view = view

        # analogous to what happens with model and parent in standard filterset
        for filter_ in self.filters.values():
            filter_.view = view


class PagedFilterSet(ClassBasedViewFilterSet):
    """Removes page parameters from the query when applying filters."""

    page_kwarg = "page"

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

    Make sure to use the DistinctOrderingFilter if the list needs to be
    paginated and ordered with an OrderingFilter
    """

    defaults = None

    def __init__(self, data, *args, **kwargs):
        data = data.copy()

        # Set the defaults if they are not manually set yet
        for key, value in self.defaults.items():
            if key not in data:
                data[key] = value
        super().__init__(data, *args, **kwargs)


class DistinctOrderingFilter(django_filters.OrderingFilter):
    """Makes sure, that every queryset gets a distinct ordering.

    Even if field to order by (e.g. comment count) would produce a non-distinct
    ordering.
    """

    def filter(self, qs, value):
        if value in django_filters.constants.EMPTY_VALUES:
            return qs.order_by("pk")

        ordering = [self.get_ordering_value(param) for param in value] + ["pk"]
        return qs.order_by(*ordering)


class DynamicChoicesOrderingFilter(DynamicChoicesMixin, DistinctOrderingFilter):
    """Used for ordering filters with dynamic choices based on view properties.

    For example dynamically add the rating ordering based on the module.
    """

    def __init__(self, *args, **kwargs):
        if "widget" not in kwargs:
            kwargs["widget"] = OrderingWidget
        kwargs["empty_label"] = None
        super().__init__(*args, **kwargs)

    def annotate_queryset(self, qs):
        qs = qs.annotate_comment_count()
        if hasattr(qs, "annotate_positive_rating_count"):
            qs = qs.annotate_positive_rating_count().annotate_negative_rating_count()
        return qs

    def filter(self, qs, value):
        annotated_qs = self.annotate_queryset(qs)
        if value == ["-comment_count"]:
            return annotated_qs.order_by("-comment_count")
        elif value == ["-positive_rating_count"]:
            return annotated_qs.order_by("-positive_rating_count")

        return super().filter(annotated_qs, value)


class DistinctOrderingWithDailyRandomFilter(DynamicChoicesOrderingFilter):
    """Note: order reproducability relies on string representation of seed."""

    def filter(self, qs, value):
        if value == ["dailyrandom"]:
            pks = list(qs.values_list("pk", flat=True))
            random.seed(str(date.today()))
            random.shuffle(pks)
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pks)])
            ordered_qs = qs.filter(pk__in=pks).order_by(preserved)
            return self.annotate_queryset(ordered_qs)
        else:
            return super().filter(qs, value)


class FreeTextFilter(django_filters.CharFilter):
    """Free text filter searches given fields.

    Set fields to search on.
    """

    def multi_filter(self, qs, name, value):
        if value:
            qs = qs.filter(reduce(operator.or_, self.get_q_objects(value)))
        return qs

    def get_q_objects(self, value):
        q_objects = [Q(((field + "__icontains"), value)) for field in self.fields]
        return q_objects

    def __init__(self, *args, **kwargs):
        kwargs["method"] = self.multi_filter

        if "fields" in kwargs:
            self.fields = kwargs.pop("fields")
        else:
            raise ImproperlyConfigured("set fields to search on")

        super().__init__(*args, **kwargs)
