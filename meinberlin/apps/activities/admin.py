from django import forms
from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget

from . import models


class ActivityAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["description"].widget = CKEditor5Widget(
            config_name="collapsible-image-editor",
        )

    class Meta:
        model = models.Activity
        fields = "__all__"


class ActivityAdmin(admin.ModelAdmin):
    form = ActivityAdminForm


admin.site.register(models.Activity, ActivityAdmin)
