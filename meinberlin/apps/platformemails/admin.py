from django.contrib import admin

from .models import PlatformEmail


@admin.register(PlatformEmail)
class PlatformEmailAdmin(admin.ModelAdmin):
    list_display = ("subject", "sent")
    date_hierarchy = "sent"
