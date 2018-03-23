from rest_framework import mixins
from rest_framework import viewsets

from adhocracy4.api.mixins import AllowPUTAsCreateMixin
from adhocracy4.api.permissions import IsModerator

from .models import ModeratorRemark
from .serializers import ModeratorRemarkSerializer


class ModeratorRemarkViewSet(AllowPUTAsCreateMixin,
                             mixins.UpdateModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):

    queryset = ModeratorRemark.objects
    serializer_class = ModeratorRemarkSerializer
    permission_classes = (IsModerator, )
    lookup_field = 'idea__slug'

    def get_permission_object(self):
        return self.remark
