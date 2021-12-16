from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from .models import TokenVote
from .models import VotingToken


class TokenVoteSerializer(serializers.ModelSerializer):
    token = serializers.PrimaryKeyRelatedField(
        queryset=VotingToken.objects.all()
    )
    content_type = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all()
    )

    class Meta:
        model = TokenVote
        fields = ['token', 'content_type', 'object_pk']
        read_only_fields = ('token', 'content_type')
