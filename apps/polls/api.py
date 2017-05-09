from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework import viewsets

from adhocracy4.api.permissions import ViewSetRulesPermission
from apps.contrib.api.mixins import AllowPUTAsCreateMixin
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


class VoteViewSet(AllowPUTAsCreateMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
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
