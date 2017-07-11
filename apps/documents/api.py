from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin

from adhocracy4.api.mixins import ModuleMixin
from adhocracy4.api.permissions import ViewSetRulesPermission

from .models import Chapter
from .serializers import DocumentSerializer


class DocumentViewSet(ModuleMixin,
                      CreateModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = DocumentSerializer
    permission_classes = (ViewSetRulesPermission,)

    def get_permission_object(self):
        return self.module

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'module_pk': int(self.module_pk),
        })
        return context

    def get_queryset(self):
        return Chapter.objects.filter(module_id=self.module_pk)
