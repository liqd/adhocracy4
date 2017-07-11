from django.contrib import admin

from . import models


@admin.register(models.Paragraph)
class ParagraphAdmin(admin.ModelAdmin):
    list_filter = ('chapter',)
    readonly_fields = ('creator',)


@admin.register(models.Chapter)
class ChapterAdmin(admin.ModelAdmin):
    readonly_fields = ('creator', )
