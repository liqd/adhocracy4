from django.conf import settings
from django.db import models

from adhocracy4.categories.form_fields import IconChoiceField
from adhocracy4.modules import models as module_models


class IconField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 254
        kwargs['default'] = ''
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        """Initialize icon choices from the settings if they exist."""

        if hasattr(settings, 'A4_CATEGORY_ICONS'):
            self.choices = settings.A4_CATEGORY_ICONS

        # Call the super method at last so that choices are already initialized
        super().contribute_to_class(cls, name, **kwargs)

    def formfield(self, **kwargs):
        form_class = kwargs.get('choices_form_class', IconChoiceField)
        kwargs['choices_form_class'] = form_class
        return super().formfield(**kwargs)


class Category(models.Model):
    name = models.CharField(max_length=120)
    icon = IconField()
    module = models.ForeignKey(
        module_models.Module,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
