from django import forms
from django.contrib import admin

from adhocracy4.categories.models import Category
from adhocracy4.labels.models import Label
from adhocracy4.modules import admin as module_admin
from meinberlin.apps.moderationtasks.models import ModerationTask

from . import models


class ItemAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = True
        self.fields['labels'].required = False
        # FIXME if can be removed once all ideas have moderation tasks
        if hasattr(self.instance, 'completed_tasks'):
            self.fields['completed_tasks'].required = False


class IdeaAdmin(module_admin.ItemAdmin):
    form = ItemAdminForm

    def has_add_permission(self, request, obj=None):
        return False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = \
                Category.objects.filter(module=self.get_module(request))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'labels':
            kwargs['queryset'] = \
                Label.objects.filter(module=self.get_module(request))
        elif db_field.name == 'completed_tasks':
            kwargs['queryset'] = \
                ModerationTask.objects.filter(module=self.get_module(request))
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_module(self, request):
        item = self.get_object(
            request, request.resolver_match.kwargs['object_id'])
        return item.module


admin.site.register(models.Idea, IdeaAdmin)
