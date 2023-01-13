from django.utils import timezone
from rest_framework import viewsets

from adhocracy4.projects.enums import Access
from meinberlin.apps.extprojects.models import ExternalProject
from meinberlin.apps.extprojects.serializers import ExternalProjectSerializer


class ExternalProjectListViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        return ExternalProject.objects.filter(
            project_type="meinberlin_extprojects.ExternalProject",
            is_draft=False,
            access=Access.PUBLIC,
            is_archived=False,
        )

    def get_serializer(self, *args, **kwargs):
        now = timezone.now()
        return ExternalProjectSerializer(now=now, *args, **kwargs)
