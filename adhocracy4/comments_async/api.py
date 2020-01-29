from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from adhocracy4.api.mixins import ContentTypeMixin
from adhocracy4.api.permissions import ViewSetRulesPermission
from adhocracy4.comments.models import Comment

from .filters import CommentCategoryFilterBackend
from .filters import CommentOrderingFilterBackend
from .filters import CustomSearchFilter
from .serializers import ThreadListSerializer
from .serializers import ThreadSerializer


class CommentSetPagination(PageNumberPagination):
    page_size = 20


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     ContentTypeMixin,
                     viewsets.GenericViewSet):

    permission_classes = (ViewSetRulesPermission,)
    filter_backends = (filters.DjangoFilterBackend,
                       CommentOrderingFilterBackend,
                       CommentCategoryFilterBackend,
                       CustomSearchFilter)
    filterset_fields = ('object_pk', 'content_type')
    ordering = ('-created')
    content_type_filter = settings.A4_COMMENTABLES
    pagination_class = CommentSetPagination
    search_fields = ('comment', '=creator__username')

    def list(self, request, content_type=None, object_pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            if 'commentID' in request.query_params:
                try:
                    commentID = int(request.query_params['commentID'])
                    if queryset.filter(id=commentID).exists():
                        response.data['comment_found'] = True
                    else:
                        parent = [item for item in
                                  queryset.values_list('id', 'child_comments')
                                  if item[1] == commentID]
                        if parent:
                            response.data['comment_found'] = True
                            response.data['comment_parent'] = parent[0][0]
                        else:
                            response.data['comment_found'] = False
                except ValueError:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            return response
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'list':
            return ThreadListSerializer
        return ThreadSerializer

    def perform_create(self, serializer):
        serializer.save(
            content_object=self.content_object,
            creator=self.request.user
        )

    def get_permission_object(self):
        return self.content_object

    def get_queryset(self):
        child_comment_content_type_id = \
            ContentType.objects.get_for_model(Comment)
        comments = Comment.objects\
            .filter(object_pk=self.object_pk)\
            .filter(content_type_id=self.content_type.pk)
        if self.action == 'list':
            return comments\
                .exclude(content_type_id=child_comment_content_type_id)\
                .order_by('-created')
        return comments

    @property
    def rules_method_map(self):
        return ViewSetRulesPermission.default_rules_method_map._replace(
            POST='{app_label}.comment_{model}'.format(
                app_label=self.content_type.app_label,
                model=self.content_type.model
            )
        )

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if self.request.user == comment.creator:
            comment.is_removed = True
        else:
            comment.is_censored = True
        comment.save()
        serializer = self.get_serializer(comment)
        return Response(serializer.data)
