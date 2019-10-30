from django.conf import settings
from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from adhocracy4.api.mixins import ContentTypeMixin
from adhocracy4.api.permissions import ViewSetRulesPermission

from .models import Rating
from .serializers import RatingSerializer


class RatingViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    ContentTypeMixin,
                    viewsets.GenericViewSet):

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (ViewSetRulesPermission,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('object_pk', 'content_type')
    content_type_filter = settings.A4_RATEABLES

    def perform_create(self, serializer):
        queryset = Rating.objects.filter(content_type_id=self.content_type.pk,
                                         creator=self.request.user,
                                         object_pk=self.content_object.pk)
        if queryset.exists():
            raise ValidationError(queryset[0].pk)
        serializer.save(
            content_object=self.content_object,
            creator=self.request.user
        )

    def get_permission_object(self):
        return self.content_object

    @property
    def rules_method_map(self):
        return ViewSetRulesPermission.default_rules_method_map._replace(
            POST='{app_label}.rate_{model}'.format(
                app_label=self.content_type.app_label,
                model=self.content_type.model
            )
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
