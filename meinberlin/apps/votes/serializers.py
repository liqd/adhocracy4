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


class VotingTokenSerializer(serializers.ModelSerializer):
    votes_left = serializers.SerializerMethodField()
    num_votes_left = serializers.SerializerMethodField()

    class Meta:
        model = VotingToken
        fields = ['votes_left', 'num_votes_left']
        read_only_fields = ('votes_left', 'num_votes_left')

    def get_votes_left(self, token):
        return token.has_votes_left

    def get_num_votes_left(self, token):
        return token.num_votes_left
