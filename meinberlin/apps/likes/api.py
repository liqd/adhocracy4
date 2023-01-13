from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework import viewsets

from adhocracy4.api.permissions import ViewSetRulesPermission
from meinberlin.apps.livequestions.models import LiveQuestion

from .models import Like
from .serializers import LikeSerializer


class LikesViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = LikeSerializer
    permission_classes = (ViewSetRulesPermission,)

    def dispatch(self, request, *args, **kwargs):
        self.question_pk = kwargs.get("question_pk", "")
        return super().dispatch(request, *args, **kwargs)

    def get_permission_object(self):
        return self.question

    def get_queryset(self):
        return Like.objects.filter(question=self.question)

    def perform_create(self, serializer):
        if not self.request.session.session_key:
            self.request.session.create()
        session = Session.objects.get(session_key=self.request.session.session_key)
        like_value = bool(self.request.data["value"])
        if like_value:
            serializer.save(session=session, question=self.question)
        elif Like.objects.filter(session=session, question=self.question).exists():
            Like.objects.get(session=session, question=self.question).delete()

    @property
    def question(self):
        return get_object_or_404(LiveQuestion, pk=self.question_pk)
