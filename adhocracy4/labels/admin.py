from django.contrib import admin

from adhocracy4.projects.admin import ProjectAdminFilter

from . import models


class ProjectFilter(ProjectAdminFilter):
    project_key = 'module__project'


class LabelAdmin(admin.ModelAdmin):
    list_filter = (
        'module__project__organisation',
        'module__project__is_archived',
        ProjectFilter
    )


admin.site.register(models.Label, LabelAdmin)
