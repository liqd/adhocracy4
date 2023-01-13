from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from adhocracy4.models.base import UserGeneratedContentModel


class ModeratorRemark(UserGeneratedContentModel):
    item_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    item_object_id = models.PositiveIntegerField()
    item = GenericForeignKey(ct_field="item_content_type", fk_field="item_object_id")

    remark = models.TextField(
        blank=True,
        verbose_name=_("Moderation remark (internal)"),
        help_text=_(
            "Here you can write a moderation remark. It is only "
            "displayed for moderators and initiators of your project."
        ),
    )

    @property
    def project(self):
        return self.item.project

    @property
    def content(self):
        if self.remark:
            return True
        else:
            return False

    class Meta:
        unique_together = ("item_content_type", "item_object_id")
