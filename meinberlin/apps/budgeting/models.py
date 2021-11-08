from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.comments import models as comment_models
from adhocracy4.projects.models import \
    ProjectContactDetailMixin as contact_mixin
from adhocracy4.ratings import models as rating_models
from meinberlin.apps.mapideas import models as mapidea_models


class Proposal(mapidea_models.AbstractMapIdea):
    ratings = GenericRelation(rating_models.Rating,
                              related_query_name='budget_proposal',
                              object_id_field='object_pk')
    comments = GenericRelation(comment_models.Comment,
                               related_query_name='budget_proposal',
                               object_id_field='object_pk')
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

    allow_contact = models.BooleanField(default=True)

    contact_email = models.EmailField(blank=True)

    contact_phone = models.CharField(blank=True,
                                     max_length=255,
                                     validators=[contact_mixin.phone_regex])

    def get_absolute_url(self):
        return reverse('meinberlin_budgeting:proposal-detail',
                       kwargs=dict(pk='{:05d}'.format(self.pk),
                                   year=self.created.year))

    class Meta:
        ordering = ['-created']
