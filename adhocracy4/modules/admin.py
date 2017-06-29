from django.contrib import admin

from adhocracy4.phases import admin as phase_admin

from . import models


class ItemAdmin(admin.ModelAdmin):
    list_filter = ('module__project', 'module')
    readonly_fields = ('creator', )


class ModuleAdmin(admin.ModelAdmin):
    inlines = [
        phase_admin.PhaseInline
    ]
    list_filter = ('project', 'project__organisation')


admin.site.register(models.Module, ModuleAdmin)
