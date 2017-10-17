from django.contrib import admin

from adhocracy4.projects import models


class ProjectAdmin(admin.ModelAdmin):
    actions = ('publish', 'archive')
    list_display = ('__str__', 'organisation', 'is_draft', 'is_archived')
    list_filter = ('is_draft', 'is_archived', 'organisation')
    raw_id_fields = ('moderators', 'participants')

    def publish(modeladmin, request, queryset):
        queryset.update(is_draft=False)

    def archive(modeladmin, request, queryset):
        queryset.update(is_archived=False)


# Overwrite adhocracy4.projects.admin
admin.site.unregister(models.Project)
admin.site.register(models.Project, ProjectAdmin)
