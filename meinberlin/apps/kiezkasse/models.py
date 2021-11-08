from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.comments import models as comment_models
from adhocracy4.ratings import models as rating_models
from meinberlin.apps.mapideas import models as mapidea_models


class Proposal(mapidea_models.AbstractMapIdea):
    ratings = GenericRelation(rating_models.Rating,
                              related_query_name='kiezkasse_proposal',
                              object_id_field='object_pk')
    comments = GenericRelation(comment_models.Comment,
                               related_query_name='kiezkasse_proposal',
                               object_id_field='object_pk')
    budget = models.PositiveIntegerField(
        default=0,
        help_text=_('Required Budget')
    )

    creator_contribution = models.BooleanField(
        default=False,
        verbose_name=_('Own contribution to the proposal'),
        help_text=_('I want to contribute to the proposal myself.')
    )

    def get_absolute_url(self):
        return reverse('meinberlin_kiezkasse:proposal-detail',
                       kwargs=dict(pk='{:05d}'.format(self.pk),
                                   year=self.created.year))

    class Meta:
        ordering = ['-created']
