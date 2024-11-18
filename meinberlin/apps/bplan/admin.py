from django.contrib import admin

from . import models


@admin.register(models.Bplan)
class BplanAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "identifier",
        "url",
        "description",
        "is_draft",
        "tile_image",
        "tile_image_alt_text",
        "tile_image_copyright",
        "is_archived",
        "point",
        "office_worker_email",
    )
    list_display = (
        "__str__",
        "identifier",
        "organisation",
        "is_draft",
        "is_archived",
        "created",
    )
    list_filter = ("is_draft", "is_archived", "organisation")
    search_fields = ("name",)
    date_hierarchy = "created"
