from rest_framework import serializers

from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    meta_info = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        read_only_fields = ('id', 'meta_info')
        exclude = ('creator', 'modified', 'created')

    def get_meta_info(self, obj):
        user = self.context['request'].user
        return obj.get_meta_info(user)
