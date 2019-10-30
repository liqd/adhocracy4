from django.contrib import admin

from adhocracy4.phases import admin as phase_admin
from adhocracy4.projects.admin import ProjectAdminFilter

from . import models


class ProjectFilter(ProjectAdminFilter):
    project_key = 'module__project'


class ItemAdmin(admin.ModelAdmin):
    list_filter = (
        'module__project__organisation',
        'module__project__is_archived',
        ProjectFilter
    )
    list_display = ('__str__', 'creator', 'created')
    readonly_fields = ('creator', )
    date_hierarchy = 'created'


class ModuleAdmin(admin.ModelAdmin):
    inlines = [
        phase_admin.PhaseInline
    ]
    list_filter = ('project__organisation', 'project')
    list_display = ('__str__', 'name')


admin.site.register(models.Module, ModuleAdmin)
