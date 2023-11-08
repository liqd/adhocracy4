from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
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
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True
