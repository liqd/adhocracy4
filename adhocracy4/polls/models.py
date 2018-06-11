from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from adhocracy4.comments import models as comment_models
from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.modules import models as module_models


class QuestionQuerySet(models.QuerySet):
    def annotate_vote_count(self):
        return self.annotate(
            vote_count=models.Count(
                'choices__votes__creator_id',
                distinct=True)
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


class Question(models.Model):
    label = models.CharField(max_length=255)
    weight = models.SmallIntegerField()
    multiple_choice = models.BooleanField(default=False)

    poll = models.ForeignKey(
        'Poll',
        on_delete=models.CASCADE,
        related_name='questions'
    )

    objects = QuestionQuerySet.as_manager()

    def user_choices_list(self, user):
        if not user.is_authenticated():
            return []

        return self.choices\
            .filter(votes__creator=user)\
            .values_list('id', flat=True)

    def get_absolute_url(self):
        return self.poll.get_absolute_url()

    def __str__(self):
        return self.label

    class Meta:
        ordering = ['weight']


class Choice(models.Model):
    label = models.CharField(max_length=255)

    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='choices',
    )

    objects = ChoiceQuerySet.as_manager()

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
