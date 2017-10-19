from django.contrib import admin

from adhocracy4.projects.admin import ProjectAdminFilter

from . import models


@admin.register(models.Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sent', 'project', 'organisation')
    list_filter = (
        'project__organisation',
        'project__is_archived',
        ProjectAdminFilter
    )
    date_hierarchy = 'sent'
