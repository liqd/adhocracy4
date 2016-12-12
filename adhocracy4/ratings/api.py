from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.response import Response

from adhocracy4.api.permissions import IsCreatorOrReadOnly

from .models import Rating
from .serializers import RatingSerializer


class RatingViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('object_pk', 'content_type')

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def destroy(self, request, pk=None):
        """
        Sets value to zero
        NOTE: Rating is NOT deleted.
        """
        rating = self.get_object()
        rating.update(0)
        serializer = self.get_serializer(rating)
        return Response(serializer.data)
