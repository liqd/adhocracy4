from django.utils import timezone
from rest_framework import viewsets

from meinberlin.apps.extprojects.models import ExternalProject
from meinberlin.apps.extprojects.serializers import ExternalProjectSerializer


class ExternalProjectListViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        return ExternalProject.objects.filter(
            is_draft=False,
            is_public=True
        )

    def get_serializer(self, *args, **kwargs):
        now = timezone.now()
        return ExternalProjectSerializer(now=now, *args, **kwargs)
