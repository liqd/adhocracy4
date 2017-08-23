def _component_sort_key(component):
    return component.weight, component.identifier


class DashboardContents:
    _registry = {'projects': {}, 'modules': {}}

    def register_project(self, component):
        self._register('projects', component)

    def register_module(self, component):
        self._register('modules', component)

    def _register(self, section, component):
        if component.identifier in self._registry[section]:
            raise ValueError('Identifier ({}) is already registered'
                             .format(component.identifier))
        self._registry[section][component.identifier] = component

    def get_project_components(self):
        return sorted(self._registry['projects'].values(),
                      key=_component_sort_key)

    def get_module_components(self):
        return sorted(self._registry['modules'].values(),
                      key=_component_sort_key)

    def get_urls(self):
        # FIXME: where to move this method
        from django.conf.urls import url

        urlpatterns = []
        for component in self.get_project_components():
            urls = component.get_urls()
            if urls:
                for pattern, view, name in urls:
                    urlpattern = url(pattern, view, name=name)
                    urlpatterns.append(urlpattern)

        for component in self.get_module_components():
            urls = component.get_urls()
            if urls:
                for pattern, view, name in urls:
                    urlpattern = url(pattern, view, name=name)
                    urlpatterns.append(urlpattern)

        return urlpatterns


content = DashboardContents()
