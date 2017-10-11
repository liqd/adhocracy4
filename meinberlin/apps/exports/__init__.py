from django.apps import apps as django_apps


def register_export(description):
    def export_view_decorator(view_cls):
        exports.register(description, view_cls)
        return lambda cls: cls
    return export_view_decorator


class ExportsRegistry:
    _registry = {}

    def register(self, description, cls):
        app_config = django_apps.get_containing_app_config(cls.__module__)
        app_label = app_config.label
        app_exports = self._registry.get(app_label, [])
        app_exports.append((description, cls))
        self._registry[app_label] = sorted(app_exports, key=lambda e: e[1])

    def __getitem__(self, module):
        return self._registry[module.phases.first().content().app]

    def __contains__(self, module):
        return module.phases.first().content().app in self._registry


exports = ExportsRegistry()
