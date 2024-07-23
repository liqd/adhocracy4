from django.core.cache import cache
from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.response import Response

from meinberlin.apps.plans.models import Plan
from meinberlin.apps.plans.serializers import PlanSerializer


def get_plans() -> QuerySet[Plan]:
    """
    Helper function to query the db and retrieve all
    plans.
    """
    return (
        Plan.objects.filter(is_draft=False)
        .select_related("organisation", "district")
        .prefetch_related("projects", "topics")
    )


class PlansListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlanSerializer

    def get_queryset(self):
        return get_plans()

    def list(self, request, *args, **kwargs):
        data = cache.get("plans")
        if data is None:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set("plans", data)

        return Response(data)
