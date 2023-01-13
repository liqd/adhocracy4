from django.contrib import admin

from . import models


@admin.register(models.ExternalProject)
class ExternalProjectAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "url",
        "description",
        "is_draft",
        "tile_image",
        "tile_image_copyright",
        "is_archived",
    )
    list_display = ("__str__", "organisation", "is_draft", "is_archived", "created")
    list_filter = ("is_draft", "is_archived", "organisation")
    search_fields = ("name",)
    date_hierarchy = "created"

    def get_queryset(self, request):
        return models.ExternalProject.objects.filter(bplan=None)
