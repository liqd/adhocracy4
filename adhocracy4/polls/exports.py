from collections import defaultdict

from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from django.db.models import Q
from django.utils.translation import gettext as _
from django.utils.translation import pgettext
from rules.contrib.views import PermissionRequiredMixin

from adhocracy4.comments.models import Comment
from adhocracy4.exports import mixins as export_mixins
from adhocracy4.exports import views as export_views
from adhocracy4.polls import models as poll_models

User = get_user_model()


class PollCommentExportView(
    PermissionRequiredMixin,
    export_mixins.ItemExportWithLinkMixin,
    export_mixins.ExportModelFieldsMixin,
    export_mixins.UserGeneratedContentExportMixin,
    export_mixins.ItemExportWithRatesMixin,
    export_mixins.CommentExportWithRepliesToMixin,
    export_views.BaseItemExportView,
):
    model = Comment

    fields = ["id", "comment", "created"]
    permission_required = "a4polls.change_poll"

    def get_permission_object(self):
        return self.module

    def get_queryset(self):
        return Comment.objects.filter(
            Q(poll__module=self.module) | Q(parent_comment__poll__module=self.module)
        ).select_related("poll", "parent_comment", "poll__module")

    def get_virtual_fields(self, virtual):
        virtual.setdefault("id", _("ID"))
        virtual.setdefault("comment", pgettext("noun", "Comment"))
        virtual.setdefault("created", _("Created"))
        return super().get_virtual_fields(virtual)

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated


class PollExportView(PermissionRequiredMixin, export_views.BaseItemExportView):
    permission_required = "a4polls.change_poll"
    CHUNK_SIZE = 2000  # Optimal for most databases

    def dispatch(self, request, *args, **kwargs):
        """Initialise data structures before processing."""
        self._init_export_data()
        return super().dispatch(request, *args, **kwargs)

    def _init_export_data(self):
        """Load all required data in batches."""
        if not hasattr(self, "_is_initialised"):
            # Core poll data (single query)
            self.poll = (
                poll_models.Poll.objects.filter(module=self.module)
                .select_related("module")
                .prefetch_related(
                    Prefetch(
                        "questions",
                        queryset=poll_models.Question.objects.prefetch_related(
                            "choices",
                            Prefetch(
                                "answers",
                                queryset=poll_models.Answer.objects.select_related(
                                    "question"
                                ),
                            ),
                        ),
                    )
                )
                .first()
            )

            # Batch-load all votes with related data
            vote_queryset = (
                poll_models.Vote.objects.filter(choice__question__poll=self.poll)
                .select_related("choice", "choice__question")
                .prefetch_related("other_vote")
            )

            # Process votes without iterator since we need all in memory
            self._votes = list(vote_queryset)

            # Batch-load other votes (single query)
            self._other_votes_map = {
                ov.vote_id: ov.answer
                for ov in poll_models.OtherVote.objects.filter(
                    vote_id__in=[v.id for v in self._votes]
                )
            }

            # Build optimised lookup structures
            self._build_lookup_structures()
            self._is_initialised = True

    def _build_lookup_structures(self):
        """Create memory-efficient access patterns for data."""
        # User -> {choice_id: vote} mapping
        self._user_votes = defaultdict(dict)
        # User -> {question_id: answer} mapping
        self._user_answers = defaultdict(dict)

        # Process votes
        for vote in self._votes:
            user_key = vote.creator_id or f"anon_{vote.content_id}"
            self._user_votes[user_key][vote.choice_id] = vote

        # Process answers from prefetched data
        for question in self.poll.questions.all():
            for answer in question.answers.all():
                user_key = answer.creator_id or f"anon_{answer.content_id}"
                self._user_answers[user_key][question.id] = answer

    def get_voters(self):
        """Get all unique voters in optimised way."""
        # Get all user keys from both structures
        user_keys = set(self._user_votes.keys()).union(set(self._user_answers.keys()))

        # Separate authenticated and anonymous
        user_ids = []
        anon_users = []

        for key in user_keys:
            if str(key).startswith("anon_"):
                anon_users.append(key.replace("anon_", ""))
            else:
                user_ids.append(int(key))

        # Bulk fetch users in single query
        user_objects = (
            {u.id: u for u in User.objects.filter(id__in=user_ids)} if user_ids else {}
        )

        # Return combined list
        return list(user_objects.values()) + anon_users

    def get_object_list(self):
        """Create optimised voter list with indexes."""
        voters = self.get_voters()
        return [(idx, voter) for idx, voter in enumerate(voters)]

    def get_virtual_fields(self, virtual):
        """Generate export fields dynamically."""
        virtual = super().get_virtual_fields(virtual)
        virtual["voter_id"] = _("Voter ID")

        for question in self.poll.questions.all():
            if question.is_open:
                virtual[(question.id, False)] = f"Q{question.id}"
                virtual[(question.id, True)] = f"Q{question.id}_text"
            else:
                for choice in question.choices.all():
                    virtual[(choice.id, False)] = f"Q{question.id}_A{choice.id}"
                    if choice.is_other_choice:
                        virtual[(choice.id, True)] = f"Q{question.id}_A{choice.id}_text"

        return virtual

    def get_field_data(self, item, field):
        """Ultra-optimised field data access."""
        index, voter = item

        # Handle voter ID
        if field == "voter_id":
            return str(index + 1) if hasattr(voter, "pk") else f"Anon{index + 1}"

        # Get unified user key
        user_key = str(voter.pk) if hasattr(voter, "pk") else f"anon_{voter}"

        # Handle question/choice fields
        field_id, is_text = field

        if isinstance(field_id, int):  # Question ID (open question)
            answer = self._user_answers.get(user_key, {}).get(field_id)
            if not is_text:
                return 1 if answer else 0
            return answer.answer if answer else ""

        else:  # Choice ID
            vote = self._user_votes.get(user_key, {}).get(field_id)
            if not is_text:
                return 1 if vote else 0
            return self._other_votes_map.get(vote.id, "") if vote else ""

    def get_permission_object(self):
        return self.module

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated
