from django.utils import timezone
from rest_framework import viewsets

from meinberlin.apps.projectcontainers.models import ProjectContainer
from meinberlin.apps.projectcontainers.serializers import \
    ProjectContainerSerializer


class ProjectContainerListViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        containers = ProjectContainer.objects.filter(
            is_draft=False,
            is_public=True,
            is_archived=False
        )
        return containers

    def get_serializer(self, *args, **kwargs):
        now = timezone.now()
        return ProjectContainerSerializer(now=now, *args, **kwargs)
