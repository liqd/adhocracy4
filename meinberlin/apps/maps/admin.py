from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from adhocracy4.maps.models import AreaSettings

from . import models

# Register your models here.
admin.site.register(models.MapPreset, admin.ModelAdmin)
admin.site.register(models.MapPresetCategory, admin.ModelAdmin)


@admin.register(AreaSettings)
class AreaSettingsAdmin(admin.ModelAdmin):
    description = 'Foo'
    list_display = ('module_name', 'project_name')

    fieldsets = (
        (None, {'fields': ('module',)}),
        (_('Polygon'), {
            'fields': ('polygon',),
            'description': _('Enter a valid GeoJSON object. An empty string is'
                             ' not valid. To initialize a new areasetting'
                             ' enter "" or false.')
        })
    )

    def module_name(self, setting):
        return setting.module.name

    def project_name(self, setting):
        return setting.module.project
