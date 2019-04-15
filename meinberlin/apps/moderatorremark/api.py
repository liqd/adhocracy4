from django.http import Http404
from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework import viewsets

from adhocracy4.api.mixins import ContentTypeMixin
from adhocracy4.api.permissions import ViewSetRulesPermission

from .models import ModeratorRemark
from .serializers import ModeratorRemarkSerializer


class AllContentTypesFilter:
    def __contains__(self, item):
        return True


class ModeratorRemarkViewSet(mixins.CreateModelMixin,
                             mixins.UpdateModelMixin,
                             ContentTypeMixin,
                             viewsets.GenericViewSet):

    queryset = ModeratorRemark.objects.all()
    serializer_class = ModeratorRemarkSerializer
    permission_classes = (ViewSetRulesPermission,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_object_id', 'item_content_type')
    content_type_filter = AllContentTypesFilter()

    def get_permission_object(self):
        return self.content_object

    def get_object(self):
        remark = super().get_object()
        # Ensure the remark belongs to the item defined by the content type
        if remark.item != self.content_object:
            raise Http404
        return remark

    def perform_create(self, serializer):
        serializer.save(
            item=self.content_object,
            creator=self.request.user
        )
