from ckeditor.fields import RichTextField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from adhocracy4.models.base import UserGeneratedContentModel

from apps.mapideas import models as mapidea_models
from apps.moderatorfeedback.fields import ModeratorFeedbackField


class Proposal(mapidea_models.AbstractMapIdea):
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
        return reverse('meinberlin_budgeting:proposal-detail',
                       args=[str(self.slug)])


class ModeratorStatement(UserGeneratedContentModel):
    proposal = models.OneToOneField(
        Proposal,
        primary_key=True,
        related_name="moderator_statement")

    statement = RichTextField(blank=True)
