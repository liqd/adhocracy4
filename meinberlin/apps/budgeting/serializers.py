from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from meinberlin.apps.votes.models import TokenVote
from meinberlin.apps.votes.models import VotingToken

from .models import Proposal


class ProposalSerializer(serializers.ModelSerializer):

    comment_count = serializers.SerializerMethodField()
    creator = serializers.SerializerMethodField()
    negative_rating_count = serializers.SerializerMethodField()
    positive_rating_count = serializers.SerializerMethodField()
    session_token_voted = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    vote_allowed = serializers.SerializerMethodField()

    class Meta:
        model = Proposal
        fields = (
            "additional_item_badges_for_list_count",
            "comment_count",
            "created",
            "creator",
            "is_archived",
            "item_badges_for_list",
            "modified",
            "name",
            "negative_rating_count",
            "pk",
            "positive_rating_count",
            "reference_number",
            "session_token_voted",
            "url",
            "vote_allowed",
        )
        read_only_fields = (
            "additional_item_badges_for_list_count",
            "comment_count",
            "created",
            "creator",
            "is_archived",
            "item_badges_for_list",
            "modified",
            "name",
            "negative_rating_count",
            "pk",
            "positive_rating_count",
            "reference_number",
            "session_token_voted",
            "url",
            "vote_allowed",
        )

    def get_creator(self, proposal):
        return proposal.creator.username

    def get_comment_count(self, proposal):
        if hasattr(proposal, "comment_count"):
            return proposal.comment_count
        else:
            return 0

    def get_positive_rating_count(self, proposal):
        if hasattr(proposal, "positive_rating_count"):
            return proposal.positive_rating_count
        else:
            return 0

    def get_negative_rating_count(self, proposal):
        if hasattr(proposal, "negative_rating_count"):
            return proposal.negative_rating_count
        else:
            return 0

    def get_url(self, proposal):
        return proposal.get_absolute_url()

    def get_session_token_voted(self, proposal):
        """Serialize if proposal has been voted.

        Returns bool that indicates whether the proposal has
        been voted with the token in the current session
        """
        if "request" in self.context:
            if "voting_tokens" in self.context["request"].session:
                module = self.context["view"].module
                module_key = str(module.id)
                if module_key in self.context["request"].session["voting_tokens"]:
                    token = VotingToken.get_voting_token_by_hash(
                        token_hash=self.context["request"].session["voting_tokens"][module_key],
                        module=module
                    )
                    if not token:
                        return False
                    vote = TokenVote.objects.filter(
                        token=token,
                        content_type=ContentType.objects.get_for_model(proposal.__class__),
                        object_pk=proposal.pk,
                    )
                    return vote.exists()
        return False

    def get_vote_allowed(self, proposal):

        if "request" in self.context:
            user = self.context["request"].user
            has_voting_permission = user.has_perm(
                "meinberlin_budgeting.vote_proposal", proposal
            )
            is_three_phase_budgeting = proposal.module.blueprint_type == "PB3"
            return has_voting_permission and is_three_phase_budgeting

        return False

    def reference_number(self, proposal):
        if hasattr(proposal, "ref_number"):
            return proposal.ref_number
        else:
            return ""
