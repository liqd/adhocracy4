from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.comments import models as comment_models
from adhocracy4.projects.models import ProjectContactDetailMixin as contact_mixin
from adhocracy4.ratings import models as rating_models
from meinberlin.apps.ideas import models as idea_models
from meinberlin.apps.mapideas import models as mapidea_models
from meinberlin.apps.moderationtasks.models import ModerationTask
from meinberlin.apps.votes.models import TokenVote


class ProposalQuerySet(idea_models.IdeaQuerySet):
    def annotate_token_vote_count(self):
        return self.annotate(
            token_vote_count=models.Count(
                "token_votes",
                distinct=True,  # needed to combine with other count annotations
            )
        )


class Proposal(mapidea_models.AbstractMapIdea):
    ratings = GenericRelation(
        rating_models.Rating,
        related_query_name="budget_proposal",
        object_id_field="object_pk",
    )
    comments = GenericRelation(
        comment_models.Comment,
        related_query_name="budget_proposal",
        object_id_field="object_pk",
    )
    token_votes = GenericRelation(
        TokenVote,
        related_query_name="budget_proposal",
        object_id_field="object_pk",
    )
    budget = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(int(1e6))],
        verbose_name=_("Budget"),
        help_text=_(
            "Please enter the estimated or actual costs for your "
            "proposal. Enter 0€ if the costs are not (yet) known. "
            'In this case, the description "budget not specified" '
            "will appear in your proposal."
        ),
    )

    is_archived = models.BooleanField(
        default=False,
        verbose_name=_("Proposal is archived (public)"),
        help_text=_(
            "Exclude this proposal from all listings by default. "
            "You can still access this proposal by using filters."
        ),
    )

    allow_contact = models.BooleanField(default=True)

    contact_email = models.EmailField(blank=True)

    contact_phone = models.CharField(
        blank=True, max_length=255, validators=[contact_mixin.phone_regex]
    )

    completed_tasks = models.ManyToManyField(
        ModerationTask,
        verbose_name=_("completed moderation tasks"),
        related_name=("%(app_label)s_" "%(class)s" "_completed"),
    )

    objects = ProposalQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse(
            "meinberlin_budgeting:proposal-detail",
            kwargs=dict(pk="{:05d}".format(self.pk), year=self.created.year),
        )

    class Meta:
        ordering = ["-created"]
