from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.mapideas import models as mapidea_models
from apps.moderatorfeedback.models import Moderateable


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
        from django.core.urlresolvers import reverse
        return reverse('meinberlin_kiezkasse:proposal-detail',
                       args=[str(self.slug)])
