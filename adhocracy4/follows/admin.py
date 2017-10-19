from django.contrib import admin

from adhocracy4.projects.admin import ProjectAdminFilter

from . import models


@admin.register(models.Follow)
class FollowAdmin(admin.ModelAdmin):
    list_filter = (
        'project__organisation',
        'project__is_archived',
        ProjectAdminFilter
    )
    list_display = ('creator', 'project', 'enabled', 'created')
    date_hierarchy = 'created'
    readonly_fields = ('creator',)
    search_fields = ('creator__email',)
