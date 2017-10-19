from django.contrib import admin

from .models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    fields = (
        'creator', 'value', 'content_type', 'content_object'
    )
    readonly_fields = ('creator', 'content_type', 'content_object')
    list_display = ('creator', 'value', 'created')
    search_fields = ('creator__email',)
    date_hierarchy = 'created'
