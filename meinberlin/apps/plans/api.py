from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response

from meinberlin.apps.plans.models import Plan
from meinberlin.apps.plans.serializers import PlanSerializer


class PlansListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlanSerializer

    def get_queryset(self):
        return Plan.objects.filter(is_draft=False).prefetch_related("projects")

    def list(self, request, *args, **kwargs):
        data = cache.get("plans")
        if data is None:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set("plans", data)

        return Response(data)
