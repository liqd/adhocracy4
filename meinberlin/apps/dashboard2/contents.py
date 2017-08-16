class DashboardContents:
    _registry = {'project': {}, 'module': {}}

    def __getitem__(self, identifier):
        component = self._registry['project'].get(identifier, None)
        if not component:
            component = self._registry['module'].get(identifier)
        return component

    def __contains__(self, identifier):
        return (identifier in self._registry['project'] or
                identifier in self._registry['module'])

    def register_project(self, component):
        self._registry['project'][component.identifier] = component

    def register_module(self, component):
        self._registry['module'][component.identifier] = component

    def get_project_components(self):
        return self._registry['project'].values()

    def get_module_components(self):
        return self._registry['module'].values()


content = DashboardContents()
