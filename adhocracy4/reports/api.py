from rest_framework import mixins, permissions, viewsets

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
        emails.send_email_to_moderators(self.request, report)
        emails.send_email_to_creator(self.request, report)
