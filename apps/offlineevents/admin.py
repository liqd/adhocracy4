from django.contrib import admin

from . import models


@admin.register(models.OfflineEvent)
class OfflineEventAdmin(admin.ModelAdmin):
    readonly_fields = ('creator', )
