from django.contrib.contenttypes.models import ContentType
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets

from adhocracy4.comments.models import Comment

from . import emails
from .models import Report
from .serializers import ReportSerializer


class ReportViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        report = serializer.save(creator=self.request.user)
        emails.ReportModeratorEmail.send(report)

        if serializer.instance.content_type == ContentType.objects.get_for_model(
            Comment
        ):
            comment = serializer.instance.content_object
            if comment.is_reviewed:
                comment.is_reviewed = False
                comment.save(ignore_modified=True)
