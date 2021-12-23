from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from adhocracy4.categories.models import Category
from meinberlin.apps.votes.models import TokenVote

from .models import Proposal


class CategoryField(serializers.Field):

    def to_internal_value(self, category):
        if category:
            return Category.objects.get(pk=category)
        else:
            return None

    def to_representation(self, category):
        return {'id': category.pk, 'name': category.name}


class ProposalSerializer(serializers.ModelSerializer):

    creator = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    positive_rating_count = serializers.SerializerMethodField()
    negative_rating_count = serializers.SerializerMethodField()
    category = CategoryField()
    url = serializers.SerializerMethodField()
    moderator_feedback = serializers.SerializerMethodField()
    session_token_voted = serializers.SerializerMethodField()

    class Meta:
        model = Proposal
        fields = ('budget', 'category', 'comment_count', 'created', 'modified',
                  'creator', 'is_archived', 'name', 'negative_rating_count',
                  'positive_rating_count', 'url', 'pk', 'moderator_feedback',
                  'point_label', 'session_token_voted')
        read_only_fields = ('budget', 'category', 'comment_count', 'created',
                            'modified', 'creator', 'is_archived', 'name',
                            'negative_rating_count', 'positive_rating_count',
                            'url', 'pk', 'moderator_feedback',
                            'point_label', 'session_token_voted')

    def get_creator(self, proposal):
        return proposal.creator.username

    def get_comment_count(self, proposal):
        if hasattr(proposal, 'comment_count'):
            return proposal.comment_count
        else:
            return 0

    def get_positive_rating_count(self, proposal):
        if hasattr(proposal, 'positive_rating_count'):
            return proposal.positive_rating_count
        else:
            return 0

    def get_negative_rating_count(self, proposal):
        if hasattr(proposal, 'negative_rating_count'):
            return proposal.negative_rating_count
        else:
            return 0

    def get_url(self, proposal):
        return proposal.get_absolute_url()

    def get_moderator_feedback(self, proposal):
        if hasattr(proposal, 'moderator_feedback'):
            return (proposal.moderator_feedback,
                    proposal.get_moderator_feedback_display())
        else:
            return None

    def get_point_label(self, proposal):
        if hasattr(proposal, 'point_label'):
            return (proposal.point_label)
        else:
            return None

    def get_session_token_voted(self, proposal):
        """Serialize if proposal has been voted.

        Returns bool that indicates whether the proposal has
        been voted with the token in the current session
        """
        if 'request' in self.context:
            if 'voting_token' in self.context['request'].session:
                vote = TokenVote.objects.filter(
                    token__pk=self.context['request'].session['voting_token'],
                    content_type=ContentType.objects.get_for_model(
                        proposal.__class__),
                    object_pk=proposal.pk
                )
                if vote.exists():
                    return True

        return False
