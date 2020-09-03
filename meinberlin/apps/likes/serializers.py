from rest_framework import serializers

from .models import Like


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id',)

    def create(self, validated_data):
        return Like.objects.get_or_create(**validated_data)
