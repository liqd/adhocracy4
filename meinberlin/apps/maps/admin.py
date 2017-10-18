from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from adhocracy4.maps.models import AreaSettings

from . import models

# Register your models here.
admin.site.register(models.MapPreset, admin.ModelAdmin)
admin.site.register(models.MapPresetCategory, admin.ModelAdmin)


# FIXME: remove this once it is available in core
@admin.register(AreaSettings)
class AreaSettingsAdmin(admin.ModelAdmin):
    list_display = ('module_name', 'project_name')

    fieldsets = (
        (None, {'fields': ('module',)}),
        (_('Polygon'), {
            'fields': ('polygon',),
            'description': _('Enter a valid GeoJSON object. '
                             'To initialize a new areasetting enter the '
                             'string "false" without quotation marks.')
        })
    )

    def module_name(self, setting):
        return setting.module.name

    def project_name(self, setting):
        return setting.module.project
