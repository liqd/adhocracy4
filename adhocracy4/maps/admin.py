from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . import models


@admin.register(models.AreaSettings)
class AreaSettingsAdmin(admin.ModelAdmin):
    list_filter = ('module__project__organisation', 'module__project')
    list_display = ('module',)

    fieldsets = (
        (None, {'fields': ('module',)}),
        (_('Polygon'), {
            'fields': ('polygon',),
            'description': _('Enter a valid GeoJSON object. '
                             'To initialize a new areasetting enter the '
                             'string "false" without quotation marks.')
        })
    )
