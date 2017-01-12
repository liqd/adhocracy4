from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.response import Response

from adhocracy4.api.permissions import IsCreatorOrReadOnly

from .models import Comment
from .serializers import ThreadSerializer


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    queryset = Comment.objects.all().order_by('-created')
    serializer_class = ThreadSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('object_pk', 'content_type')

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if self.request.user == comment.creator:
            comment.is_removed = True
        else:
            comment.is_censored = True
        comment.save()
        serializer = self.get_serializer(comment)
        return Response(serializer.data)
