from django.db import models

from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.modules import models as module_models


class Poll(module_models.Item):
    title = models.CharField(max_length=255)
    weight = models.SmallIntegerField()

    def __str__(self):
        return self.title


class Choice(models.Model):
    label = models.CharField(max_length=255)

    poll = models.ForeignKey(
        'Poll',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '%s @%s' % (self.label, self.poll)


class Vote(UserGeneratedContentModel):
    choice = models.ForeignKey(
        'Choice',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('creator', 'choice')

    def __str__(self):
        return '%s: %s' % (self.creator, self.choice)
