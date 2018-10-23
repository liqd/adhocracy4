from django.db import models


class AdministrativeDistrict(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
