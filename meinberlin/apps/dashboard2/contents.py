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
        return list(self._registry['projects'].values())

    def get_module_components(self):
        return list(self._registry['modules'].values())

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
