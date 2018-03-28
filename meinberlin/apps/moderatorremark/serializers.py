from rest_framework import serializers

from .models import ModeratorRemark


class ModeratorRemarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeratorRemark
        read_only_fields = (
            'id', 'item_content_type', 'item_object_id'
        )
        fields = (
            'remark',
            'id', 'item_content_type', 'item_object_id'
        )
