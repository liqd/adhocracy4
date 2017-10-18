from django.contrib import admin

from adhocracy4.phases import admin as phase_admin

from . import models
from adhocracy4.projects.admin import ProjectAdminFilter


class ProjectFilter(ProjectAdminFilter):
    project_key = 'module__project'


class ItemAdmin(admin.ModelAdmin):
    list_filter = (
        'module__project__organisation',
        'module__project__is_archived',
        ProjectFilter
    )
    readonly_fields = ('creator', )


class ModuleAdmin(admin.ModelAdmin):
    inlines = [
        phase_admin.PhaseInline
    ]
    list_filter = ('project', 'project__organisation')


admin.site.register(models.Module, ModuleAdmin)
