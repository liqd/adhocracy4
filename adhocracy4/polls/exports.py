from django.contrib.auth import get_user_model
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

    def dispatch(self, request, *args, **kwargs):
        """Preload all necessary data before processing."""
        response = super().dispatch(request, *args, **kwargs)
        self._load_export_data()
        return response

    def _load_export_data(self):
        """Load all data needed for export if not already loaded."""
        if not hasattr(self, "_all_votes"):
            # Load all votes with their related data
            self._all_votes = list(self.get_queryset())

            # Load all answers with their questions
            self._all_answers = list(self.get_answers())

            # Create lookup dictionaries for faster access
            self._other_votes_dict = {
                ov.vote_id: ov.answer
                for ov in poll_models.OtherVote.objects.filter(
                    vote_id__in=[v.id for v in self._all_votes]
                )
            }

    def get_permission_object(self):
        return self.module

    def get_queryset(self):
        return (
            poll_models.Vote.objects.filter(choice__question__poll=self.poll)
            .select_related("choice", "choice__question")
            .prefetch_related("other_vote")  # Prefetch related other_vote
        )

    def get_answers(self):
        return poll_models.Answer.objects.filter(
            question__poll=self.poll
        ).select_related("question")

    def get_voters(self):
        # Get all distinct voter IDs (registered users)
        user_vote_ids = set(
            self.get_queryset()
            .exclude(creator=None)
            .values_list("creator_id", flat=True)
            .distinct()
        )

        user_answer_ids = set(
            self.get_answers()
            .exclude(creator=None)
            .values_list("creator_id", flat=True)
            .distinct()
        )

        # Combine and get all user objects in one query
        all_user_ids = user_vote_ids.union(user_answer_ids)
        users = list(User.objects.filter(pk__in=all_user_ids))

        # Get anonymous voters
        anon_vote_ids = set(
            self.get_queryset()
            .filter(creator=None)
            .values_list("content_id", flat=True)
            .distinct()
        )

        anon_answer_ids = set(
            self.get_answers()
            .filter(creator=None)
            .values_list("content_id", flat=True)
            .distinct()
        )

        anon_ids = list(anon_vote_ids.union(anon_answer_ids))

        return users + anon_ids

    def get_object_list(self):
        """Create indexed list of voters."""
        return [(index, user) for index, user in enumerate(self.get_voters())]

    @property
    def poll(self):
        """Cached poll property to avoid repeated queries."""
        if not hasattr(self, "_poll"):
            self._poll = poll_models.Poll.objects.get(module=self.module)
        return self._poll

    @property
    def questions(self):
        if not hasattr(self, "_questions"):
            self._questions = self.poll.questions.prefetch_related(
                "choices", "answers"
            ).all()
        return self._questions

    def get_virtual_fields(self, virtual):
        """Generate export fields for all questions."""
        virtual = super().get_virtual_fields(virtual)
        virtual["user_id"] = "user"

        for question in self.questions:
            if question.is_open:
                virtual = self.get_virtual_field_open_question(virtual, question)
            else:
                virtual = self.get_virtual_field_choice_question(virtual, question)

        return virtual

    def get_virtual_field_choice_question(self, virtual, choice_question):
        """Generate export fields for choice questions."""
        for choice in choice_question.choices.all():
            identifier = "Q" + str(choice_question.pk) + "_A" + str(choice.pk)
            virtual[(choice, False)] = identifier
            if choice.is_other_choice:
                identifier_answer = identifier + "_text"
                virtual[(choice, True)] = identifier_answer
        return virtual

    def get_virtual_field_open_question(self, virtual, open_question):
        """Generate export fields for open questions."""
        identifier = "Q" + str(open_question.pk)
        virtual[(open_question, False)] = identifier
        identifier_answer = identifier + "_text"
        virtual[(open_question, True)] = identifier_answer
        return virtual

    def get_field_data(self, item, field):
        """Ensure data is loaded before field access."""
        self._load_export_data()

        index, user = item

        if field == "user_id":
            # Handle user ID display
            return str(index + 1) if hasattr(user, "pk") else f"Anon{index + 1}"

        field_object, is_text_field = field

        if isinstance(field_object, poll_models.Choice):
            # Handle choice-based fields
            user_filter = (
                ("creator_id", user.pk)
                if hasattr(user, "pk")
                else ("creator", None, "content_id", user)
            )

            # Find matching votes in preloaded data
            matching_votes = [
                v
                for v in self._all_votes
                if v.choice_id == field_object.id
                and self._match_user_filter(v, user_filter)
            ]

            if not is_text_field:
                return int(bool(matching_votes))
            elif matching_votes:
                return self._other_votes_dict.get(matching_votes[0].id, "")
            return ""
        else:
            # Handle question-based fields (open answers)
            user_filter = (
                ("creator_id", user.pk)
                if hasattr(user, "pk")
                else ("creator", None, "content_id", user)
            )

            # Find matching answers in preloaded data
            matching_answers = [
                a
                for a in self._all_answers
                if a.question_id == field_object.id
                and self._match_user_filter(a, user_filter)
            ]

            if not is_text_field:
                return int(bool(matching_answers))
            elif matching_answers:
                return matching_answers[0].answer
            return ""

    def _match_user_filter(self, obj, user_filter):
        """Helper to check if object matches user filter criteria."""
        if len(user_filter) == 2:  # Registered user case
            attr, value = user_filter
            return getattr(obj, attr) == value
        else:  # Anonymous user case
            return (
                obj.creator is None and getattr(obj, user_filter[2]) == user_filter[3]
            )
