from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from adhocracy4.models.base import UserGeneratedContentModel


class ModeratorRemark(UserGeneratedContentModel):
    item_content_type = models.ForeignKey(ContentType, null=True,
                                          blank=True)
    item_object_id = models.PositiveIntegerField()
    item = GenericForeignKey('item_content_type', 'item_object_id')

    remark = models.CharField(max_length=200,
                              verbose_name=_('Remark'),
                              blank=True)

    class Meta:
        unique_together = ('item_content_type', 'item_object_id', 'remark')
