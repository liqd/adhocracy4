from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from meinberlin.apps.mapideas import models as mapidea_models
from meinberlin.apps.moderatorfeedback.models import Moderateable


class Proposal(mapidea_models.AbstractMapIdea, Moderateable):
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
