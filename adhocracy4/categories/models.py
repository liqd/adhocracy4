from django.db import models

from adhocracy4.modules import models as module_models


class Category(models.Model):
    name = models.CharField(max_length=120)
    module = models.ForeignKey(
        module_models.Module,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
