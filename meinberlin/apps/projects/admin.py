from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from adhocracy4.projects import models
from adhocracy4.projects.admin import ProjectAdminForm


@admin.action(description=_("archive"))
def set_is_archived_true(modeladmin, request, queryset):
    queryset.update(is_archived=True)


@admin.action(description=_("dearchive"))
def set_is_archived_false(modeladmin, request, queryset):
    queryset.update(is_archived=False)


class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = (
        "__str__",
        "slug",
        "organisation",
        "is_draft",
        "is_archived",
        "project_type",
        "created",
    )
    list_filter = ("is_draft", "is_archived", "organisation")
    search_fields = ("name",)
    raw_id_fields = ("moderators", "participants")
    date_hierarchy = "created"

    actions = [
        set_is_archived_true,
        set_is_archived_false,
    ]

    fieldsets = (
        (None, {"fields": ("name", "slug", "organisation", "group")}),
        (
            _("Topic and location"),
            {
                "fields": ("topics", "point", "administrative_district"),
            },
        ),
        (
            _("Information and result"),
            {
                "fields": ("description", "information", "result"),
            },
        ),
        (
            _("Settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    "access",
                    "is_draft",
                    "is_archived",
                    "moderators",
                    "participants",
                    "project_type",
                ),
            },
        ),
        (
            _("Images"),
            {
                "classes": ("collapse",),
                "fields": (
                    "image",
                    "image_copyright",
                    "tile_image",
                    "tile_image_alt_text",
                    "tile_image_copyright",
                ),
            },
        ),
        (
            _("Contact"),
            {
                "classes": ("collapse",),
                "fields": (
                    "contact_name",
                    "contact_address_text",
                    "contact_phone",
                    "contact_email",
                    "contact_url",
                ),
            },
        ),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "administrative_district":
            kwargs["empty_label"] = _("City wide")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Overwrite adhocracy4.projects.admin
admin.site.unregister(models.Project)
admin.site.register(models.Project, ProjectAdmin)
