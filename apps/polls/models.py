from django.db import models

from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.modules import models as module_models


class Poll(models.Model):
    title = models.CharField(max_length=255)

    module = models.ForeignKey(
        module_models.Module,
        on_delete=models.CASCADE,
    )


class Choice(models.Model):
    label = models.CharField(max_length=255)

    poll = models.ForeignKey(
        'Poll',
        on_delete=models.CASCADE,
    )


class Vote(UserGeneratedContentModel):
    poll = models.ForeignKey(
        'Poll',
        on_delete=models.CASCADE,
    )

    choice = models.ForeignKey(
        'Choice',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('creator', 'poll', 'choice')
