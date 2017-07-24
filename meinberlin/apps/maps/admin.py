from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.MapPreset, admin.ModelAdmin)
admin.site.register(models.MapPresetCategory, admin.ModelAdmin)
