from django.db.models import Count
from django.db import models

from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.modules import models as module_models


class Poll(module_models.Item):
    title = models.CharField(max_length=255)
    weight = models.SmallIntegerField()

    def choices_with_vote_count(self):
        return self.choices\
            .annotate(vote__count=Count('votes'))\
            .filter(poll=self)

    def __str__(self):
        return self.title


class Choice(models.Model):
    label = models.CharField(max_length=255)

    poll = models.ForeignKey(
        'Poll',
        on_delete=models.CASCADE,
        related_name='choices',
    )

    @property
    def vote_count(self):
        if hasattr(self, 'vote__count'):
            return self.vote__count
        return self.votes.count()

    def __str__(self):
        return '%s @%s' % (self.label, self.poll)


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
