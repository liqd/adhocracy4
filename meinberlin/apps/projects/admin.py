from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from adhocracy4.projects import models


def set_is_archived_true(modeladmin, request, queryset):
    queryset.update(is_archived=True)


set_is_archived_true.short_description = _('archive')


def set_is_archived_false(modeladmin, request, queryset):
    queryset.update(is_archived=False)


set_is_archived_false.short_description = _('dearchive')


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'organisation', 'is_draft', 'is_archived', 'created'
    )
    list_filter = ('is_draft', 'is_archived', 'organisation')
    search_fields = ('name',)
    raw_id_fields = ('moderators', 'participants')
    date_hierarchy = 'created'

    actions = [
        set_is_archived_true,
        set_is_archived_false,
    ]

    fieldsets = (
        (None, {
            'fields': ('name', 'organisation')
        }),
        (_('Topic and location'), {
            'fields': ('topics', 'point', 'administrative_district'),
        }),
        (_('Information and result'), {
            'fields': ('description', 'information', 'result'),
        }),
        (_('Settings'), {
            'classes': ('collapse',),
            'fields': ('is_public', 'is_draft', 'is_archived',
                       'moderators', 'participants')
        }),
        (_('Images'), {
            'classes': ('collapse',),
            'fields': ('image', 'image_copyright', 'tile_image',
                       'tile_image_copyright')
        }),
        (_('Contact'), {
            'classes': ('collapse',),
            'fields': ('contact_name', 'contact_address_text',
                       'contact_phone', 'contact_email', 'contact_url'),
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'administrative_district':
            kwargs['empty_label'] = _('City wide')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Overwrite adhocracy4.projects.admin
admin.site.unregister(models.Project)
admin.site.register(models.Project, ProjectAdmin)
