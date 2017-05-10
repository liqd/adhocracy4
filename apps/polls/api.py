from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.request import clone_request
from rest_framework.response import Response

from adhocracy4.api.permissions import ViewSetRulesPermission
from .models import Poll
from .models import Question
from .models import Vote
from .serializers import PollSerializer
from .serializers import VoteSerializer


class PollViewSet(mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (ViewSetRulesPermission,)

    def get_permission_object(self):
        poll = self.get_object()
        return poll.module


class VoteViewSetRulesPermission(ViewSetRulesPermission):
    """Ensures the permission object is returned on update."""

    non_object_actions = ['list', 'create', 'update']


class VoteViewSet(viewsets.GenericViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (VoteViewSetRulesPermission,)

    def dispatch(self, request, *args, **kwargs):
        self.question_pk = int(kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    @property
    def question(self):
        return get_object_or_404(
            Question,
            pk=self.question_pk
        )

    def get_object(self):
        return get_object_or_404(
            Vote,
            creator=self.request.user,
            choice__question=self.question_pk
        )

    def get_permission_object(self):
        return self.question.poll.module

    def get_serializer_context(self):
        context = super(VoteViewSet, self).get_serializer_context()
        context.update({
            'question_pk': self.question_pk,
        })
        return context

    def update(self, request, *args, **kwargs):
        # Based on the a4-opin AllowPUTAsCreateMixin.
        #
        # Since this view has a mismatch between its pk (which is
        # related to questions) and its serializer (which is related to votes)
        # the AllowPUTAsCreateMixin won't work correctly, as it sets the pk
        # on the serializer object which obviously results in faulty database
        # operations.
        partial = kwargs.pop('partial', False)

        instance = self.get_object_or_none()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)

        if instance is None:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        serializer.save()
        return Response(serializer.data)

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            if self.request.method == 'PUT':
                # For PUT-as-create operation, we need to ensure that we have
                # relevant permissions, as if this was a POST request.  This
                # will either raise a PermissionDenied exception, or simply
                # return None.
                self.check_permissions(clone_request(self.request, 'POST'))
            else:
                # PATCH requests where the object does not exist should still
                # return a 404 response.
                raise
