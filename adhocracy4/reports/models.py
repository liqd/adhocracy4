from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from adhocracy4.models import base


class Report(base.UserGeneratedContentModel):

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_pk = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        ct_field="content_type", fk_field="object_pk")
    description = models.TextField(max_length=1024)

    def __str__(self):
        return "{}_{}".format(str(self.content_type), str(self.object_pk))

    class Meta:
        index_together = [('content_type', 'object_pk')]

    @property
    def project(self):
        co = self.content_object
        return co.project
