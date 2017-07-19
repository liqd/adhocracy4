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

    def get_absolute_url(self):
        return reverse('meinberlin_budgeting:proposal-detail',
                       args=[str(self.slug)])

    class Meta:
        ordering = ['-created']
