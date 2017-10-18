from django.contrib import admin

from . import models


@admin.register(models.Bplan)
class BplanAdmin(admin.ModelAdmin):
    fields = (
        'name', 'url', 'description', 'tile_image', 'tile_image_copyright',
        'is_archived', 'office_worker_email'
    )
    list_display = ('__str__', 'organisation', 'is_draft', 'is_archived')
    list_filter = ('is_draft', 'is_archived', 'organisation')
    search_fields = ('name',)
    date_hierarchy = 'created'
