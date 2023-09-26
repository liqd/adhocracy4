from rest_framework import viewsets

from meinberlin.apps.plans.models import Plan
from meinberlin.apps.plans.serializers import PlanSerializer


class PlansListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlanSerializer

    def get_queryset(self):
        return Plan.objects.filter(is_draft=False).prefetch_related("projects")
