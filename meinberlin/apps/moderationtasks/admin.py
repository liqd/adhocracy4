from django.contrib import admin

from . import models


class ModerationTaskAdmin(admin.ModelAdmin):
    list_filter = (
        "module__project__organisation",
        "module__project__is_archived",
        "module__project",
        "module",
    )
    list_display = ("__str__", "module")


admin.site.register(models.ModerationTask, ModerationTaskAdmin)
