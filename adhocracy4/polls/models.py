from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from adhocracy4.comments import models as comment_models
from adhocracy4.models.base import GeneratedContentModel
from adhocracy4.modules import models as module_models
from adhocracy4.polls import validators


class QuestionQuerySet(models.QuerySet):
    """Queryset which can annotate the Question model with different counts of a vote
    vote_count: counts the number of people who have voted on the question
    vote_count_multi: counts the total numer of votes on the question
    answer_count: counts the number of people which answered an open question
    """

    def annotate_vote_count(self):
        return self.annotate(
            vote_count=models.Count("choices__votes__creator__id", distinct=True)
            + models.Count("choices__votes__content_id", distinct=True),
            vote_count_multi=models.Count("choices__votes", distinct=True),
            answer_count=models.Count("answers__creator__id", distinct=True)
            + models.Count("answers__content_id", distinct=True),
        ).order_by("weight")


class ChoiceQuerySet(models.QuerySet):
    def annotate_vote_count(self):
        return self.annotate(vote_count=models.Count("votes"))


class Poll(module_models.Item):
    allow_unregistered_users = models.BooleanField(default=False)
    comments = GenericRelation(
        comment_models.Comment, related_query_name="poll", object_id_field="object_pk"
    )

    def get_absolute_url(self):
        return self.module.get_detail_url

    def annotated_questions(self):
        return self.questions.annotate_vote_count()


class Question(models.Model):
    label = models.CharField(max_length=255)
    help_text = models.CharField(
        max_length=250, blank=True, verbose_name=_("Explanation")
    )

    weight = models.SmallIntegerField()

    multiple_choice = models.BooleanField(default=False)
    is_open = models.BooleanField(default=False)

    poll = models.ForeignKey("Poll", on_delete=models.CASCADE, related_name="questions")

    objects = QuestionQuerySet.as_manager()

    @property
    def has_other_option(self):
        return self.choices.filter(is_other_choice=True).exists()

    def get_other_option(self):
        if self.has_other_option:
            return self.choices.filter(is_other_choice=True).first()
        return None

    def clean(self, *args, **kwargs):
        if self.is_open:
            if self.multiple_choice:
                raise ValidationError(
                    {
                        "is_open": _(
                            "Questions with open answers cannot "
                            "have multiple choices."
                        )
                    }
                )
            elif Choice.objects.filter(question=self.pk).count() > 0:
                raise ValidationError(
                    {
                        "is_open": _(
                            "Question with choices cannot become "
                            "open question. Delete choices or add new "
                            "open question."
                        )
                    }
                )

        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def user_choices_list(self, user):
        if not user.is_authenticated:
            return []

        return self.choices.filter(votes__creator=user).values_list("id", flat=True)

    def user_answer(self, user) -> int | str:
        """Returns the id of the Answer the user gave to the question or an empty
        string."""
        if user.is_authenticated:
            answers = self.answers.filter(creator=user)
            if answers.exists():
                # there can only be one answer bc of unique constraint
                return answers.first().id
        return ""

    def other_choice_answers(self):
        if self.has_other_option:
            other_choice = self.choices.filter(is_other_choice=True).first()
            other_answers = OtherVote.objects.filter(vote__choice=other_choice)
            return other_answers
        else:
            return OtherVote.objects.none()

    def other_choice_user_answer(self, user):
        """Returns the id of the 'other' answer the user gave to the question or an empty
        string."""
        if user.is_authenticated and self.has_other_option:
            other_choice = self.choices.filter(is_other_choice=True).first()
            other_choice_user_answer = OtherVote.objects.filter(
                vote__creator=user, vote__choice=other_choice
            )
            if other_choice_user_answer.exists():
                # there can only be one other vote as 1:1 relation
                return other_choice_user_answer.first().vote.id
        return ""

    def get_absolute_url(self):
        return self.poll.get_absolute_url()

    def __str__(self):
        return self.label

    class Meta:
        ordering = ["weight"]


class Answer(GeneratedContentModel):
    answer = models.CharField(max_length=750, verbose_name=_("Answer"))

    question = models.ForeignKey(
        "Question",
        on_delete=models.CASCADE,
        related_name="answers",
    )

    def clean(self, *args, **kwargs):
        if not self.question.is_open:
            raise ValidationError(
                {"question": _("Only open questions can have answers.")}
            )
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.question.poll.get_absolute_url()

    def __str__(self):
        return "%s: %s" % (self.creator, self.answer[:20])

    class Meta:
        ordering = ["id"]
        unique_together = ("question", "creator", "content_id")


class Choice(models.Model):
    label = models.CharField(max_length=255)

    question = models.ForeignKey(
        "Question",
        on_delete=models.CASCADE,
        related_name="choices",
    )

    is_other_choice = models.BooleanField(default=False)

    weight = models.SmallIntegerField()

    objects = ChoiceQuerySet.as_manager()

    def clean(self, *args, **kwargs):
        if self.question.is_open:
            raise ValidationError({"label": _("Open questions cannot have choices.")})
        elif self.is_other_choice:
            if self.question.choices.count() == 0:
                raise ValidationError(
                    {
                        "is_other_choice": _(
                            '"Other" cannot be the only choice. '
                            "Use open question or add more "
                            "choices."
                        )
                    }
                )
            if (
                self.question.has_other_option
                and self.id != self.question.get_other_option().id
            ):
                raise ValidationError(
                    {"is_other_choice": _('Question already has "other" ' "choice.")}
                )
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.question.poll.get_absolute_url()

    def __str__(self):
        return "%s @%s" % (self.label, self.question)

    class Meta:
        ordering = ["weight", "id"]


class Vote(GeneratedContentModel):
    choice = models.ForeignKey("Choice", on_delete=models.CASCADE, related_name="votes")

    def save(self, *args, **kwargs):
        self.validate_unique()
        return super().save(*args, **kwargs)

    def validate_unique(self, exclude=None):
        super().validate_unique(exclude)
        validators.single_vote_per_user(
            self.creator, self.content_id, self.choice, self.pk
        )

    @property
    def is_other_vote(self):
        return hasattr(self, "other_vote")

    # Make Vote instances behave like items for rule checking
    @property
    def module(self):
        return self.choice.question.poll.module

    @property
    def project(self):
        return self.module.project

    def get_absolute_url(self):
        return self.choice.question.poll.get_absolute_url()

    def __str__(self):
        return "%s: %s" % (self.creator, self.choice)


class OtherVote(models.Model):
    vote = models.OneToOneField(
        Vote, on_delete=models.CASCADE, primary_key=True, related_name="other_vote"
    )

    answer = models.CharField(max_length=250, verbose_name=_("Answer"))

    def clean(self, *args, **kwargs):
        if not self.vote.choice.is_other_choice:
            raise ValidationError(
                {
                    "vote": _(
                        "Other vote can only be created for vote on " '"other" choice.'
                    )
                }
            )
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def module(self):
        return self.vote.choice.question.poll.module

    @property
    def project(self):
        return self.module.project

    def get_absolute_url(self):
        return self.vote.choice.question.poll.get_absolute_url()

    def __str__(self):
        return "%s: %s" % (self.vote.creator, _("other"))
