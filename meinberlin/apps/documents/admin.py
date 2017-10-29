from django.contrib import admin

from adhocracy4.projects.admin import ProjectAdminFilter

from . import models


class ParagraphProjectFilter(ProjectAdminFilter):
    project_key = 'chapter__module__project'


@admin.register(models.Paragraph)
class ParagraphAdmin(admin.ModelAdmin):
    list_filter = (
        'chapter__module__project__organisation',
        'chapter__module__project__is_archived',
        ParagraphProjectFilter
    )
    list_display = ('__str__', 'name', 'chapter', 'created')
    readonly_fields = ('creator',)
    date_hierarchy = 'created'


class ChapterProjectFilter(ProjectAdminFilter):
    project_key = 'module__project'


@admin.register(models.Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_filter = (
        'module__project__organisation',
        'module__project__is_archived',
        ChapterProjectFilter
    )
    list_display = ('__str__', 'name', 'created')
    readonly_fields = ('creator', )
    date_hierarchy = 'created'
