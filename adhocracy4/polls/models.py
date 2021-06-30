from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from adhocracy4.comments import models as comment_models
from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.modules import models as module_models


class QuestionQuerySet(models.QuerySet):
    def annotate_vote_count(self):
        return self.annotate(
            vote_count=models.Count(
                'choices__votes__creator_id',
                distinct=True),
            vote_count_multi=models.Count(
                'choices__votes',
                distinct=True),
            answer_count=models.Count(
                'answers__creator_id',
                distinct=True),
        )


class ChoiceQuerySet(models.QuerySet):
    def annotate_vote_count(self):
        return self.annotate(
            vote_count=models.Count(
                'votes'
            )
        )


class Poll(module_models.Item):
    comments = GenericRelation(comment_models.Comment,
                               related_query_name='poll',
                               object_id_field='object_pk')

    def get_absolute_url(self):
        return self.project.get_absolute_url()

    def annotated_questions(self):
        return self.questions.annotate_vote_count()


class Question(models.Model):
    label = models.CharField(max_length=255)
    help_text = models.CharField(
        max_length=250,
        blank=True,
        verbose_name=_('Help text')
    )

    weight = models.SmallIntegerField()

    multiple_choice = models.BooleanField(default=False)
    is_open = models.BooleanField(default=False)

    poll = models.ForeignKey(
        'Poll',
        on_delete=models.CASCADE,
        related_name='questions'
    )

    objects = QuestionQuerySet.as_manager()

    @property
    def has_other_option(self):
        return self.choices.filter(is_other_choice=True).exists()

    def clean(self, *args, **kwargs):
        if self.is_open:
            if self.multiple_choice:
                raise ValidationError({
                    'is_open': _('Questions with open answers cannot '
                                 'have multiple choices.')
                })
            elif self.choices.count() > 0:
                raise ValidationError({
                    'is_open': _('Question with choices cannot become '
                                 'open question. Delete choices or add new '
                                 'open question.')
                })

        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def user_choices_list(self, user):
        if not user.is_authenticated:
            return []

        return self.choices\
            .filter(votes__creator=user)\
            .values_list('id', flat=True)

    def user_answer(self, user):
        if not user.is_authenticated:
            return ''

        answers = self.answers.filter(creator=user)
        if answers.exists():
            # there can only be one answer bc of unique constraint
            return answers.first().id
        else:
            return ''

    def other_choice_answers(self):
        if self.has_other_option:
            other_choice = self.choices.filter(is_other_choice=True).first()
            other_answers = OtherVote.objects.filter(vote__choice=other_choice)
            return other_answers
        else:
            return OtherVote.objects.none()

    def other_choice_user_answer(self, user):
        if not user.is_authenticated:
            return ''

        elif self.has_other_option:
            other_choice = self.choices.filter(is_other_choice=True).first()
            other_choice_user_answer = OtherVote.objects.filter(
                vote__creator=user,
                vote__choice=other_choice)
            if other_choice_user_answer.exists():
                # there can only be one other vote as 1:1 relation
                return other_choice_user_answer.first().vote.id
        return ''

    def get_absolute_url(self):
        return self.poll.get_absolute_url()

    def __str__(self):
        return self.label

    class Meta:
        ordering = ['weight']


class Answer(UserGeneratedContentModel):
    answer = models.CharField(
        max_length=750,
        verbose_name=_('Answer')
    )

    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='answers',
    )

    def clean(self, *args, **kwargs):
        if not self.question.is_open:
            raise ValidationError({
                'question': _('Only open questions can have answers.')
            })
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.question.poll.get_absolute_url()

    def __str__(self):
        return '%s: %s' % (self.creator, self.answer[:20])

    class Meta:
        ordering = ['id']
        unique_together = ('question', 'creator')


class Choice(models.Model):
    label = models.CharField(max_length=255)

    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='choices',
    )

    is_other_choice = models.BooleanField(default=False)

    objects = ChoiceQuerySet.as_manager()

    def clean(self, *args, **kwargs):
        if self.question.is_open:
            raise ValidationError({
                'question': _('Open questions cannot have choices.')
            })
        if self.is_other_choice and self.question.choices.count() == 0:
            raise ValidationError({
                'is_other_choice': _('"Other" cannot be the only choice. Use '
                                     'open question or add more choices.')
            })
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.question.poll.get_absolute_url()

    def __str__(self):
        return '%s @%s' % (self.label, self.question)

    class Meta:
        ordering = ['id']


class Vote(UserGeneratedContentModel):
    choice = models.ForeignKey(
        'Choice',
        on_delete=models.CASCADE,
        related_name='votes'
    )

    @property
    def is_other_vote(self):
        return hasattr(self, 'other_vote')

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
        return '%s: %s' % (self.creator, self.choice)


class OtherVote(models.Model):
    vote = models.OneToOneField(
        Vote,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='other_vote'
    )

    answer = models.CharField(
        max_length=250,
        verbose_name=_('Answer')
    )

    def clean(self, *args, **kwargs):
        if not self.vote.choice.is_other_choice:
            raise ValidationError({
                'vote': _('Other vote can only be created for vote on '
                          '"other" choice.')
            })
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
        return '%s: %s' % (self.vote.creator, _('other'))
