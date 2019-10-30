from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets

from adhocracy4.api.mixins import AllowPUTAsCreateMixin

from . import models
from .serializers import FollowSerializer


class FollowViewSet(AllowPUTAsCreateMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    lookup_field = 'project__slug'
    queryset = models.Follow.objects
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('enabled', )

    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)
