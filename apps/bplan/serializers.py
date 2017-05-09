from django.conf import settings
from django.db.models.loading import get_model

from rest_framework import serializers

from .models import Bplan


class BplanSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    typ = serializers.HiddenField(default='Bplan')
    is_draft = serializers.HiddenField(default=False)

    class Meta:
        model = Bplan
        fields = (
            'id', 'name', 'description', 'is_archived', 'url',
            'office_worker_email', 'typ', 'is_draft'
        )

    def create(self, validated_data):
        orga_pk = self._context.get('organisation_pk', None)
        orga_model = get_model(settings.A4_ORGANISATIONS_MODEL)
        orga = orga_model.objects.get(pk=orga_pk)
        validated_data['organisation'] = orga
        return super().create(validated_data)
