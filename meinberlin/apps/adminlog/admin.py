from itertools import chain

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import components
from adhocracy4.projects.admin import ProjectAdminFilter

from .models import LogEntry


class ComponentFilter(admin.SimpleListFilter):
    title = _("Component")
    parameter_name = "component_identifier"

    def lookups(self, request, model_admin):
        return chain(
            (
                (component.identifier, component.label)
                for component in components.projects.values()
            ),
            (
                (component.identifier, component.label)
                for component in components.modules.values()
            ),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(component_identifier=self.value())


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    readonly_fields = (
        "timestamp",
        "action",
        "actor",
        "message",
        "project",
        "module",
        "component",
    )
    exclude = ("component_identifier",)

    list_filter = (
        "action",
        "project__organisation",
        ProjectAdminFilter,
        ComponentFilter,
    )
    list_display = ("timestamp", "message", "actor", "action", "project", "component")
    date_hierarchy = "timestamp"

    @admin.display(description=_("Component"))
    def component(self, instance):
        if not instance.component_identifier:
            return ""

        if instance.component_identifier in components.projects:
            component = components.projects[instance.component_identifier]
            return component.label
        elif instance.component_identifier in components.modules:
            component = components.modules[instance.component_identifier]
            return component.label

        return ""
