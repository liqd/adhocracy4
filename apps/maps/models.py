from django.db import models

from adhocracy4.maps import fields as map_fields


class MapPresetCategory(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class MapPreset(models.Model):
    name = models.CharField(max_length=128)
    polygon = map_fields.MultiPolygonField()
    category = models.ForeignKey(MapPresetCategory,
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL,)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
