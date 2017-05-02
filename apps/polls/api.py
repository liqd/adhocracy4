from rest_framework import mixins
from rest_framework import viewsets

from adhocracy4.api.mixins import ModuleMixin
from adhocracy4.api.permissions import ViewSetRulesPermission

from .models import Poll
from .serializers import PollSerializer


class PollViewSet(mixins.UpdateModelMixin,
                  ModuleMixin,
                  viewsets.GenericViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (ViewSetRulesPermission,)

    def get_permission_object(self):
        return self.module

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'module_pk': self.module_pk,
        })
        return context
