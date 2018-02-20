from django.db import models
from django.utils.translation import ugettext_lazy as _

from adhocracy4.models.base import UserGeneratedContentModel
from meinberlin.apps.ideas import models as idea_models


class ModeratorRemark(UserGeneratedContentModel):
    idea = models.ForeignKey(idea_models.Idea, null=True)
    remark = models.CharField(max_length=200,
                              verbose_name=_('Remark'),
                              blank=True)

    class Meta:
        unique_together = ('idea', 'remark')
