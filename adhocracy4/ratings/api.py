from django.conf import settings

from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.response import Response

from adhocracy4.api.mixins import ContentTypeMixin
from adhocracy4.api.permissions import IsCreatorOrReadOnly

from .models import Rating
from .serializers import RatingSerializer


class RatingViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    ContentTypeMixin,
                    viewsets.GenericViewSet):

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('object_pk', 'content_type')
    content_type_filter = settings.A4_RATEABLES

    def perform_create(self, serializer):
        serializer.save(
            content_object=self.content_object,
            creator=self.request.user
        )

    def destroy(self, request, content_type, object_pk, pk=None):
        """
        Sets value to zero
        NOTE: Rating is NOT deleted.
        """
        rating = self.get_object()
        rating.update(0)
        serializer = self.get_serializer(rating)
        return Response(serializer.data)
