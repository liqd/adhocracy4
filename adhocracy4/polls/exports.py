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

    def get_permission_object(self):
        return self.module

    def get_queryset(self):
        creators_vote = poll_models.Vote.objects.filter(
            choice__question__poll=self.poll
        ).values_list("creator", flat=True)
        creators_answer = poll_models.Answer.objects.filter(
            question__poll=self.poll
        ).values_list("creator", flat=True)
        creator_ids = list(set(creators_vote).union(set(creators_answer)))
        return User.objects.filter(pk__in=creator_ids)

    def get_object_list(self):
        # index is needed for (anonymous) user id
        return [(index, user) for index, user in enumerate(self.get_queryset().all())]

    @property
    def poll(self):
        return poll_models.Poll.objects.get(module=self.module)

    @property
    def questions(self):
        return self.poll.questions.all()

    def get_virtual_fields(self, virtual):
        virtual = super().get_virtual_fields(virtual)
        virtual["user_id"] = "user"
        for question in self.questions:
            if question.is_open:
                virtual = self.get_virtual_field_open_question(virtual, question)
            else:
                virtual = self.get_virtual_field_choice_question(virtual, question)

        return virtual

    def get_virtual_field_choice_question(self, virtual, choice_question):
        for choice in choice_question.choices.all():
            identifier = "Q" + str(choice_question.pk) + "_A" + str(choice.pk)
            virtual[(choice, False)] = identifier
            if choice.is_other_choice:
                identifier_answer = identifier + "_text"
                virtual[(choice, True)] = identifier_answer

        return virtual

    def get_virtual_field_open_question(self, virtual, open_question):
        identifier = "Q" + str(open_question.pk)
        virtual[(open_question, False)] = identifier
        identifier_answer = identifier + "_text"
        virtual[(open_question, True)] = identifier_answer

        return virtual

    def get_field_data(self, item, field):
        index, user = item

        if field == "user_id":
            value = index + 1

        else:
            field_object, is_text_field = field
            if isinstance(field_object, poll_models.Choice):
                votes_qs = poll_models.Vote.objects.filter(
                    choice=field_object, creator=user
                )
                if not is_text_field:
                    value = int(votes_qs.exists())
                else:
                    vote = votes_qs.first()
                    if vote:
                        value = poll_models.OtherVote.objects.get(vote=vote).answer
                    else:
                        value = ""
            else:  # field_object is question
                answers_qs = poll_models.Answer.objects.filter(
                    question=field_object, creator=user
                )
                if not is_text_field:
                    value = int(answers_qs.exists())
                else:
                    answer = answers_qs.first()
                    if answer:
                        value = answer.answer
                    else:
                        value = ""

        return value
