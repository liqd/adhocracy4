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
        app_name = app_config.name
        app_exports = self._registry.get(app_name, [])
        app_exports.append((description, cls))
        self._registry[app_name] = sorted(app_exports, key=lambda e: e[1])

    def __getitem__(self, module):
        phase_content = module.phases.first().content()
        app_config = django_apps.get_app_config(phase_content.app)
        return self._registry[app_config.name]

    def __contains__(self, module):
        try:
            self[module]
            return True
        except AttributeError:
            return False


exports = ExportsRegistry()
