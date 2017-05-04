from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from adhocracy4.api.mixins import ModuleMixin
from adhocracy4.api.permissions import ViewSetRulesPermission

from .models import Choice
from .models import Poll
from .models import Vote
from .serializers import PollSerializer
from .serializers import VoteSerializer


class PollViewSet(mixins.UpdateModelMixin,
                  ModuleMixin,
                  viewsets.GenericViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (ViewSetRulesPermission,)

    def get_object(self):
        # Ensure the poll belongs to the module defined in the url
        return Poll.objects.get(module=self.module,
                                pk=self.module_pk)

    def get_permission_object(self):
        return self.module

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'module_pk': self.module_pk,
        })
        return context


class VoteViewSet(mixins.CreateModelMixin,
                  ModuleMixin,
                  viewsets.GenericViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (ViewSetRulesPermission,)

    def get_permission_object(self):
        return self.module

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'module_pk': self.module_pk,
        })
        return context

    def create(self, request, *args, **kwargs):
        """
        Create a vote for the given choice.

        If a vote for the current user already exists, update it instead.
        """
        # Try to get the users current vote for the question
        # related to the submitted choice
        try:
            choice = Choice.objects.get(pk=request.data['choice'])
            instance = Vote.objects.get(
                creator=request.user,
                choice__question=choice.question)
        except Exception:
            instance = None

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if instance:
            response_status = status.HTTP_200_OK
            headers = None
        else:
            response_status = status.HTTP_201_CREATED
            headers = self.get_success_headers(serializer.data)

        return Response(serializer.data,
                        headers=headers,
                        status=response_status)
