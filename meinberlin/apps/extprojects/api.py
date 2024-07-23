from django.core.cache import cache
from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response

from adhocracy4.projects.enums import Access
from meinberlin.apps.extprojects.models import ExternalProject
from meinberlin.apps.extprojects.serializers import ExternalProjectSerializer


def get_external_projects() -> QuerySet[ExternalProject]:
    """
    Helper function to query the db and retrieve all
    external projects.
    """
    return (
        ExternalProject.objects.filter(
            project_type="meinberlin_extprojects.ExternalProject",
            is_draft=False,
            access=Access.PUBLIC,
            is_archived=False,
        )
        .select_related("organisation")
        .prefetch_related("topics")
    )


class ExternalProjectListViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        return get_external_projects()

    def get_serializer(self, *args, **kwargs):
        now = timezone.now()
        return ExternalProjectSerializer(now=now, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        data = cache.get("extprojects")
        if data is None:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set("extprojects", data)

        return Response(data)
