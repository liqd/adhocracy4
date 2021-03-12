from django import forms
from django.contrib import admin

from adhocracy4.modules import admin as module_admin

from . import models


class ItemAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['labels'].required = False


class IdeaAdmin(module_admin.ItemAdmin):
    form = ItemAdminForm

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(models.Idea, IdeaAdmin)
