from django.contrib import admin

from . import models


class ParagraphAdmin(admin.ModelAdmin):
    list_filter = ('document',)


admin.site.register(models.Document)
admin.site.register(models.Paragraph, ParagraphAdmin)
