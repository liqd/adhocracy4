class DashboardContents:
    _registry = {'projects': {}, 'modules': {}}

    @property
    def projects(self):
        return self._registry['projects']

    @property
    def modules(self):
        return self._registry['modules']

    def register_project(self, component):
        self._registry['projects'][component.identifier] = component

    def register_module(self, component):
        self._registry['modules'][component.identifier] = component

    def get_project_components(self):
        return self._registry['projects'].values()

    def get_module_components(self):
        return self._registry['modules'].values()


content = DashboardContents()
