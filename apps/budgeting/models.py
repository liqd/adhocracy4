from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.ideas import models as idea_models
from apps.moderatorfeedback.fields import ModeratorFeedbackField


class Proposal(idea_models.AbstractIdea):
    budget = models.PositiveIntegerField(
        default=0,
        help_text=_('Required Budget')
    )

    moderator_feedback = ModeratorFeedbackField(
        choices=(
            ('CONSIDERATION', _('Under consideration')),
            ('REJECTED', _('Rejected')),
            ('ACCEPTED', _('Accepted'))
        )
    )

    def get_absolute_url(self):
        return reverse('budgeting:proposal-detail', args=[str(self.slug)])
