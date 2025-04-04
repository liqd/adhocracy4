from django import forms
from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.widgets import CKEditor5Widget

from . import models


class ProjectAdminFilter(admin.SimpleListFilter):
    title = _("Project")
    parameter_name = "project"
    project_key = "project"

    def lookups(self, request, model_admin):
        projects = models.Project.objects.all()

        organisation_param = self.project_key + "__organisation__id__exact"
        org = request.GET.get(organisation_param)
        if org is not None:
            projects = projects.filter(organisation=org)

        archived_param = self.project_key + "__is_archived__exact"
        is_archived = request.GET.get(archived_param)
        if is_archived is not None:
            projects = projects.filter(is_archived=is_archived)

        return ((p.pk, str(p)) for p in projects)

    def queryset(self, request, queryset):
        if self.value():
            query = {}
            query[self.project_key] = self.value()
            return queryset.filter(**query)


class ProjectAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["information"].widget = CKEditor5Widget(
            config_name="collapsible-image-editor"
        )
        self.fields["result"].widget = CKEditor5Widget(
            config_name="collapsible-image-editor"
        )

    class Meta:
        model = models.Project
        fields = "__all__"


class ProjectAdmin(GISModelAdmin):
    form = ProjectAdminForm
    filter_horizontal = ("moderators", "participants")
    list_display = ("__str__", "organisation", "is_draft", "is_archived", "created")
    list_filter = ("is_draft", "is_archived", "organisation")
    search_fields = ("name",)
    date_hierarchy = "created"
    gis_widget_kwargs = {
        "attrs": {
            "default_zoom": 12,  # Configure zoom level
        }
    }

    fieldsets = (
        (None, {"fields": ("name", "slug", "organisation")}),
        (
            _("Information and result"),
            {
                "fields": ("description", "information", "result"),
            },
        ),
        (
            _("Settings"),
            {
                "fields": (
                    "access",
                    "is_draft",
                    "is_archived",
                    "moderators",
                    "participants",
                )
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


admin.site.register(models.Project, ProjectAdmin)
