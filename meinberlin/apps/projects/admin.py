from django.contrib import admin

from adhocracy4.projects import models


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'organisation', 'is_draft', 'is_archived', 'created'
    )
    list_filter = ('is_draft', 'is_archived', 'organisation')
    search_fields = ('name',)
    raw_id_fields = ('moderators', 'participants')
    date_hierarchy = 'created'


# Overwrite adhocracy4.projects.admin
admin.site.unregister(models.Project)
admin.site.register(models.Project, ProjectAdmin)
