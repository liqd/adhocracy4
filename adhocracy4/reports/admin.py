from django.contrib import admin

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    fields = ('content_type', 'content_object', 'description', 'creator')
    readonly_fields = ('creator', 'content_type', 'content_object')
    list_display = ('__str__', 'creator', 'created')
    date_hierarchy = 'created'
