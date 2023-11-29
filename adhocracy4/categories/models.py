from django.db import models
from django.utils.translation import gettext_lazy as _

from adhocracy4.categories.form_fields import IconChoiceField
from adhocracy4.modules import models as module_models


class IconField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 254
        kwargs["default"] = ""
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        form_class = kwargs.get("choices_form_class", IconChoiceField)
        kwargs["choices_form_class"] = form_class
        return super().formfield(**kwargs)


class CategoryAlias(models.Model):
    title = models.CharField(
        blank=False,
        default=_("Category"),
        max_length=25,
        verbose_name=_("Type of category"),
        help_text=_(
            "You can individualise the term category. "
            "The character limit is max. 25 characters "
            "(with spaces)."
        ),
    )
    description = models.CharField(
        blank=False,
        default=_(
            "Assign your proposal to a category. "
            "This automatically appears in the display of "
            "your proposal. The list of all proposals "
            "can be filtered by category."
        ),
        max_length=300,
        verbose_name=_("Description/Helptext"),
        help_text=_(
            "You can individualise the description text. "
            "The description text is displayed to the "
            "participants as help text when they have to "
            "assign their ideas. The character limit is max. "
            "300 characters (with spaces)."
        ),
    )
    module = models.ForeignKey(
        module_models.Module,
        on_delete=models.CASCADE,
    )

    class Meta:
        # fixme: change to category with next migration
        verbose_name_plural = "categorie alias"
        ordering = ["pk"]

    def __str__(self):
        return self.title

    @staticmethod
    def get_category_alias(module):
        try:
            return CategoryAlias.objects.get(module=module)
        except CategoryAlias.DoesNotExist:
            return None


class Category(models.Model):
    name = models.CharField(max_length=120)
    icon = IconField()
    module = models.ForeignKey(
        module_models.Module,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["pk"]

    def __str__(self):
        return self.name
