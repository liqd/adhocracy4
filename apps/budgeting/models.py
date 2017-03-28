from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.ideas import models as idea_models


class Proposal(idea_models.AbstractIdea):
    budget = models.PositiveIntegerField(
        default=0,
        help_text=_('Required Budget')
    )

    def get_absolute_url(self):
        return reverse('proposal-detail', args=[str(self.slug)])
