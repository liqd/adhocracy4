from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from adhocracy4.models.base import UserGeneratedContentModel

from . import fields

DEFAULT_CHOICES = (
    ('CONSIDERATION', _('Under consideration')),
    ('REJECTED', _('Rejected')),
    ('ACCEPTED', _('Accepted')),
)


class ModeratorStatement(UserGeneratedContentModel):
    statement = RichTextField(blank=True)


class Moderateable(models.Model):
    moderator_feedback_choices = DEFAULT_CHOICES

    moderator_feedback = fields.ModeratorFeedbackField()

    moderator_statement = models.OneToOneField(
        ModeratorStatement,
        related_name='+',
        null=True,
    )

    class Meta:
        abstract = True
