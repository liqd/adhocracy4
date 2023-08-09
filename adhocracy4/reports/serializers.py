from rest_framework import serializers

from adhocracy4.api.dates import get_datetime_display

from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, source="creator.username")
    created = serializers.SerializerMethodField(required=False)

    def get_created(self, report):
        return get_datetime_display(datetime=report.created)

    class Meta:
        model = Report
        fields = [
            "username",
            "created",
            "object_pk",
            "description",
            "content_type",
        ]
