from django.conf import settings
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):

    created = models.DateTimeField(editable=False, default=timezone.now)
    modified = models.DateTimeField(blank=True, null=True, editable=False)

    class Meta:
        abstract = True

    def save(self, ignore_modified=False, *args, **kwargs):
        if self.pk is not None and not ignore_modified:
            self.modified = timezone.now()
        super(TimeStampedModel, self).save(*args, **kwargs)


class UserGeneratedContentModel(TimeStampedModel):

    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    class Meta:
        abstract = True
