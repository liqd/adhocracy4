import warnings

from django.conf import settings
from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response

from adhocracy4.api.mixins import ContentTypeMixin
from adhocracy4.api.permissions import ViewSetRulesPermission

from .models import Comment
from .serializers import CommentModerateSerializer
from .serializers import ThreadSerializer
from .signals import comment_removed


class CommentViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    ContentTypeMixin,
    viewsets.GenericViewSet,
):

    """Attention: This class is deprecated, use
    comments_async.api.CommentViewSet instead"""

    queryset = Comment.objects.all().order_by("-created")
    serializer_class = ThreadSerializer
    permission_classes = (ViewSetRulesPermission,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("object_pk", "content_type")
    content_type_filter = settings.A4_COMMENTABLES

    def perform_create(self, serializer):

        warnings.warn(
            "comments.api.CommentViewSet is deprecated, "
            "use comments_async.api.CommentViewSet",
            DeprecationWarning,
        )

        serializer.save(content_object=self.content_object, creator=self.request.user)

    def get_permission_object(self):
        return self.content_object

    @property
    def rules_method_map(self):
        return ViewSetRulesPermission.default_rules_method_map._replace(
            POST="{app_label}.comment_{model}".format(
                app_label=self.content_type.app_label, model=self.content_type.model
            )
        )

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if self.request.user == comment.creator:
            comment.is_removed = True
        else:
            comment.is_censored = True
        comment.save()
        comment_removed.send(sender=type(comment), instance=comment)
        serializer = self.get_serializer(comment)

        return Response(serializer.data)


class CommentModerateSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    ContentTypeMixin,
    viewsets.GenericViewSet,
):

    queryset = Comment.objects.all().order_by("-created")
    serializer_class = CommentModerateSerializer
    permission_classes = (ViewSetRulesPermission,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("object_pk", "content_type")
    content_type_filter = settings.A4_COMMENTABLES

    def get_permission_object(self):
        return self.content_object

    @property
    def rules_method_map(self):
        return ViewSetRulesPermission.default_rules_method_map._replace(
            POST="a4_comments.moderate_comment",
            PUT="a4_comments.moderate_comment",
            PATCH="a4_comments.moderate_comment",
            DELETE="a4_comments.moderate_comment",
        )
