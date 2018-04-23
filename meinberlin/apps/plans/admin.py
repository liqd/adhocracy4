from django.contrib import admin

from . import models


@admin.register(models.Plan)
class OfflineEventAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'organisation', 'created')

    date_hierarchy = 'created'
    search_fields = ('title',)
    readonly_fields = ('creator', )
