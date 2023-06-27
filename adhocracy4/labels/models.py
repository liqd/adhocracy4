from django.db import models
from django.utils.translation import gettext_lazy as _

from adhocracy4.modules import models as module_models


class LabelAlias(models.Model):
    title = models.CharField(
        blank=False,
        default=_("Label"),
        max_length=25,
        verbose_name=_("Type of label"),
        help_text=_(
            "You can individualise the term label. "
            "The character limit is max. 25 characters "
            "(with spaces)."
        ),
    )
    description = models.CharField(
        blank=False,
        default=_(
            "Specify your proposal with one or "
            "more labels. These will automatically "
            "appear in the display of your proposal. "
            "In addition, the list of all proposals "
            "can be filtered by labels."
        ),
        max_length=300,
        verbose_name=_("Description/Helptext"),
        help_text=_(
            "You can individualise the description "
            "text. The description text is displayed "
            "to the participants as help text when they "
            "have to assign their ideas. The character "
            "limit is max. 300 characters (with spaces)."
        ),
    )
    module = models.ForeignKey(
        module_models.Module,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = "label alias"
        ordering = ["pk"]

    def __str__(self):
        return self.title

    @staticmethod
    def get_label_alias(module):
        try:
            return LabelAlias.objects.get(module=module)
        except LabelAlias.DoesNotExist:
            return None


class Label(models.Model):
    name = models.CharField(max_length=120)
    module = models.ForeignKey(
        module_models.Module,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = "labels"
        ordering = ["pk"]

    def __str__(self):
        return self.name
