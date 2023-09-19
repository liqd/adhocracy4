from django import forms
from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget

from adhocracy4.projects.admin import ProjectAdminFilter

from . import models


class OfflineEventAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["description"].widget = CKEditor5Widget(
            config_name="collapsible-image-editor",
        )

    class Meta:
        model = models.OfflineEvent
        fields = "__all__"


@admin.register(models.OfflineEvent)
class OfflineEventAdmin(admin.ModelAdmin):
    form = OfflineEventAdminForm
    list_display = ("__str__", "project", "date", "created")
    list_filter = ("project__organisation", "project__is_archived", ProjectAdminFilter)
    date_hierarchy = "created"
    search_fields = ("name",)
    readonly_fields = ("creator",)
