from django.db import models
from django.db.models import Count

from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.modules import models as module_models


class Poll(module_models.Item):
    pass


class Question(models.Model):
    label = models.CharField(max_length=255)
    weight = models.SmallIntegerField()

    poll = models.ForeignKey(
        'Poll',
        on_delete=models.CASCADE,
        related_name='questions'
    )

    def choices_with_vote_count(self):
        return self.choices\
            .filter(question=self)\
            .annotate(vote__count=Count('votes'))

    def user_choices_list(self, user):
        return self.choices\
            .filter(question=self)\
            .filter(votes__creator=user)\
            .values_list('id', flat=True)

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

    @property
    def vote_count(self):
        if hasattr(self, 'vote__count'):
            return self.vote__count
        return self.votes.count()

    def __str__(self):
        return '%s @%s' % (self.label, self.question)


class Vote(UserGeneratedContentModel):
    choice = models.ForeignKey(
        'Choice',
        on_delete=models.CASCADE,
        related_name='votes'
    )

    class Meta:
        unique_together = ('creator', 'choice')

    def __str__(self):
        return '%s: %s' % (self.creator, self.choice)
