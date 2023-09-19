from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from adhocracy4 import transforms
from adhocracy4.models.base import UserGeneratedContentModel

from . import fields

DEFAULT_CHOICES = (
    ("CONSIDERATION", _("Under consideration")),
    ("QUALIFIED", _("Qualified for next phase")),
    ("REJECTED", _("Rejected")),
    ("ACCEPTED", _("Accepted")),
)


class ModeratorFeedback(UserGeneratedContentModel):
    feedback_text = CKEditor5Field(
        blank=True,
        verbose_name=_("Feedback (public)"),
        help_text=_(
            "The feedback appears below the idea or proposal, indicating "
            "your organisation. The creator of the contribution receives a "
            "notification."
        ),
    )

    def save(self, *args, **kwargs):
        self.feedback_text = transforms.clean_html_field(self.feedback_text)
        super().save(*args, **kwargs)


class Moderateable(models.Model):
    moderator_status_choices = DEFAULT_CHOICES

    moderator_status = fields.ModeratorFeedbackField(
        verbose_name=_("Status (public)"),
        help_text=_(
            "The status appears below the idea or proposal in red, yellow or "
            "green. The creator of the contribution receives a notification."
        ),
    )

    moderator_feedback_text = models.OneToOneField(
        ModeratorFeedback,
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
