import json

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from adhocracy4.api.mixins import ModuleMixin
from adhocracy4.api.permissions import ViewSetRulesPermission

from .models import LiveQuestion
from .serializers import LiveQuestionSerializer


class LiveQuestionViewSet(
    ModuleMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):

    serializer_class = LiveQuestionSerializer
    permission_classes = (ViewSetRulesPermission,)
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_fields = ("is_answered", "is_live", "is_hidden")
    ordering_fields = ("like_count",)

    def get_permission_object(self):
        return self.module

    def get_queryset(self):
        live_questions = (
            LiveQuestion.objects.filter(module=self.module)
            .order_by("created")
            .annotate_like_count()
        )
        if not self.request.user.has_perm(
            "meinberlin_livequestions.moderate_livequestions", self.module
        ):
            live_questions = live_questions.filter(is_hidden=False)
        return live_questions

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            body = json.loads(request.body.decode("utf-8"))
            kwargs["category"] = body["category"]
        return super().dispatch(request, *args, **kwargs)
