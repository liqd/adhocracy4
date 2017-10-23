from django.contrib import admin

from . import models


@admin.register(models.Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sent', 'project', 'organisation')
    list_filter = ('organisation', )
    date_hierarchy = 'sent'
