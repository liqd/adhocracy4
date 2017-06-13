from django.contrib import admin

from . import models


class ParagraphAdmin(admin.ModelAdmin):
    list_filter = ('chapter',)


admin.site.register(models.Chapter)
admin.site.register(models.Paragraph, ParagraphAdmin)
