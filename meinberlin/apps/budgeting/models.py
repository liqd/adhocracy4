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

    is_archived = models.BooleanField(
        default=False,
        verbose_name=_('Proposal is archived'),
        help_text=_('Exclude this proposal from all listings by default. '
                    'You can still access this proposal by using filters.'),
    )

    def get_absolute_url(self):
        return reverse('meinberlin_budgeting:proposal-detail',
                       kwargs=dict(pk='{:05d}'.format(self.pk),
                                   year=self.created.year))

    class Meta:
        ordering = ['-created']
