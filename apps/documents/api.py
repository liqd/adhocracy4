from rest_framework import mixins
from rest_framework import viewsets

from adhocracy4.api.mixins import ModuleMixin
from adhocracy4.api.permissions import ViewSetRulesPermission

from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      ModuleMixin,
                      viewsets.GenericViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (ViewSetRulesPermission,)

    def get_permission_object(self):
        return self.module
