from collections import defaultdict

from django.contrib.auth import get_user_model
from django.db.models import Prefetch
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
        comments = Comment.objects.filter(
            poll__module=self.module
        ) | Comment.objects.filter(parent_comment__poll__module=self.module)
        return comments

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
        """Load all required data including open answers."""
        if not hasattr(self, "_is_initialized"):
            self.poll = (
                poll_models.Poll.objects.filter(module=self.module)
                .select_related("module")
                .first()
            )

            # Load questions with choices and answers
            self.questions = self.poll.questions.prefetch_related(
                "choices",
                Prefetch(
                    "answers",
                    queryset=poll_models.Answer.objects.select_related("question"),
                ),
            ).all()

            # Load votes
            self._votes = list(
                poll_models.Vote.objects.filter(
                    choice__question__poll=self.poll
                ).select_related("choice", "choice__question")
            )

            # Load other votes
            self._other_votes_map = {
                ov.vote_id: ov.answer
                for ov in poll_models.OtherVote.objects.filter(
                    vote_id__in=[v.id for v in self._votes]
                )
            }

            # Build lookup structures including answers
            self._build_lookup_structures()
            self._is_initialized = True

    def _build_lookup_structures(self):
        """Create lookup structures for votes AND answers."""
        self._user_votes = defaultdict(dict)
        self._user_answers = defaultdict(dict)

        # Process votes
        for vote in self._votes:
            user_key = (
                str(vote.creator_id) if vote.creator_id else f"anon_{vote.content_id}"
            )
            self._user_votes[user_key][vote.choice_id] = vote

        # Process answers (for open questions)
        for question in self.questions.filter(is_open=True):  # Only open questions
            for answer in question.answers.all():
                user_key = (
                    str(answer.creator_id)
                    if answer.creator_id
                    else f"anon_{answer.content_id}"
                )
                # Store with question.id as key
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
        """Generate export fields with clear identifiers."""
        virtual = super().get_virtual_fields(virtual)
        virtual["voter_id"] = _("Voter ID")

        if not hasattr(self, "questions"):
            self._init_export_data()

        # For open questions
        for question in self.questions.filter(is_open=True):
            virtual[(question.id, True)] = question.label

        # For choice questions
        for question in self.questions.filter(is_open=False):
            for choice in question.choices.all():
                virtual[(choice.id, False)] = f"{question.label} - {choice.label}"
                if choice.is_other_choice:
                    virtual[(choice.id, True)] = f"{question.label} - Other (specify)"

        return virtual

    def get_field_data(self, item, field):
        """Final corrected implementation that handles all cases properly."""
        index, voter = item

        # Handle voter ID
        if field == "voter_id":
            return str(index + 1) if hasattr(voter, "pk") else f"Anon{index + 1}"

        # Get unified user key
        user_key = str(voter.pk) if hasattr(voter, "pk") else f"anon_{voter}"

        field_id, is_text = field

        # First check if this is an open question answer
        if any(q.id == field_id and q.is_open for q in self.questions):
            answer = self._user_answers.get(user_key, {}).get(field_id)
            if is_text:
                return answer.answer if answer else ""
            return 1 if answer else 0

        # Then handle choice questions
        vote = self._user_votes.get(user_key, {}).get(field_id)
        if not is_text:
            return 1 if vote else 0
        return self._other_votes_map.get(vote.id, "") if vote else ""

    def get_permission_object(self):
        return self.module

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated
