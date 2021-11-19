import secrets

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.utils import IntegrityError
from django.utils.translation import gettext_lazy as _

from adhocracy4.models import base
from adhocracy4.modules.models import Module
from adhocracy4.phases.predicates import has_feature_active


def get_token():
    return secrets.token_urlsafe(16)


class VotingToken(models.Model):

    token = models.CharField(
        max_length=40,
        primary_key=True,
        default=get_token,
        editable=False
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE
    )
    allowed_votes = models.PositiveSmallIntegerField(
        default=5
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_('Designates whether this token should be treated as '
                    'active. Unselect this instead of deleting tokens.')
    )

    # if token already exists, try to generate another one
    def save(self, *args, **kwargs):
        for i in range(4):
            try:
                super().save(*args, **kwargs)
                return
            except IntegrityError as e:
                if 'UNIQUE constraint failed' in e.args[0]:
                    if i == 3:
                        raise
                    else:
                        self.token = get_token()
                else:
                    raise

    @property
    def votes(self):
        return TokenVote.objects.filter(token=self)

    @property
    def num_votes_left(self):
        num_votes = self.votes.count()
        return self.allowed_votes - num_votes

    @property
    def has_votes_left(self):
        return self.num_votes_left > 0

    @property
    def project(self):
        return self.module.project

    # model needs to be passed as phase features are connected to models
    def is_valid(self, model):
        return (has_feature_active(self.module, model, 'vote')
                and self.is_active)

    def is_valid_for_item(self, item):
        return item.module == self.module and self.is_valid(item.__class__)


class TokenVote(base.TimeStampedModel):

    token = models.ForeignKey(
        VotingToken,
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_pk = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        ct_field="content_type",
        fk_field="object_pk"
    )

    class Meta:
        unique_together = ('content_type', 'object_pk', 'token')
        index_together = [('content_type', 'object_pk')]

    # this should then happen in the api view
    def clean(self, *args, **kwargs):
        if not self.token.is_valid_for_item(self.content_object):
            raise ValidationError({
                'token': _('This token is not valid. It might be expired '
                           'or not valid for this project.')
            })
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
