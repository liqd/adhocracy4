from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """Base model which stores the date and time of its creation and its last
    modification"""

    created = models.DateTimeField(
        verbose_name=_("Created"),
        editable=False,
        default=timezone.now,
    )
    modified = models.DateTimeField(
        verbose_name=_("Modified"),
        blank=True,
        null=True,
        editable=False,
    )

    class Meta:
        abstract = True

    def save(self, ignore_modified=False, update_fields=None, *args, **kwargs):
        if self.pk is not None and not ignore_modified:
            self.modified = timezone.now()
            if update_fields:
                update_fields = {"modified"}.union(update_fields)
        super().save(update_fields=update_fields, *args, **kwargs)


class UserGeneratedContentModel(TimeStampedModel):
    """Base model for all content created by registered users on the platform. The
    user who created the content is stored in the creator field."""

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class GeneratedContentModel(TimeStampedModel):
    """Base model for content on the platform created by unregistered or registered
    users. The tie to the user who created it is optional. For content from
    unregistered users the content_id field can be used to differentiate between
    different users. This can be useful for example to count the number of
    unregistered participants in a poll."""

    content_id = models.UUIDField(null=True, blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        abstract = True
