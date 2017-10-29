from django.contrib import admin

from adhocracy4.projects.admin import ProjectAdminFilter

from . import models


@admin.register(models.OfflineEvent)
class OfflineEventAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'project', 'date', 'created')
    list_filter = (
        'project__organisation',
        'project__is_archived',
        ProjectAdminFilter
    )
    date_hierarchy = 'created'
    search_fields = ('name',)
    readonly_fields = ('creator', )
