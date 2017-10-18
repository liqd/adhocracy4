from django.contrib import admin

from . import models


@admin.register(models.Paragraph)
class ParagraphAdmin(admin.ModelAdmin):
    list_filter = ('chapter',)
    list_display = ('__str__', 'name', 'chapter', 'created')
    readonly_fields = ('creator',)
    date_hierarchy = 'created'


@admin.register(models.Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_filter = ('module__project__organisation', 'module__project')
    list_display = ('__str__', 'name', 'created')
    readonly_fields = ('creator', )
    date_hierarchy = 'created'
