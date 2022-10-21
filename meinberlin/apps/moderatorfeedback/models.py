from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _

from adhocracy4 import transforms
from adhocracy4.models.base import UserGeneratedContentModel

from . import fields

DEFAULT_CHOICES = (
    ('CONSIDERATION', _('Under consideration')),
    ('CHECKED', _('Checked')),
    ('REJECTED', _('Rejected')),
    ('ACCEPTED', _('Accepted')),
)


class ModeratorStatement(UserGeneratedContentModel):
    statement = RichTextField(
        blank=True,
        verbose_name=_('Official feedback'),
        help_text=_(
            'The official feedback will appear below the idea, '
            'indicating your organisation. The idea provider receives '
            'a notification.')
    )

    def save(self, *args, **kwargs):
        self.statement = transforms.clean_html_field(self.statement)
        super().save(*args, **kwargs)


class Moderateable(models.Model):
    moderator_feedback_choices = DEFAULT_CHOICES

    moderator_feedback = fields.ModeratorFeedbackField(
        verbose_name=_('Processing status'),
        help_text=_(
            'The editing status appears below the title of the '
            'idea in red, yellow or green. The idea provider receives a '
            'notification.')
    )

    moderator_statement = models.OneToOneField(
        ModeratorStatement,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True
