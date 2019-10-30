from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets

from . import emails
from .models import Report
from .serializers import ReportSerializer


class ReportViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        report = serializer.save(creator=self.request.user)
        emails.ReportModeratorEmail.send(report)
