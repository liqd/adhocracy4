from adhocracy4.phases import content as phases_content


class ModuleContent:
    @property
    def identifier(self):
        return '{s.app}:module'.format(s=self)

    def __str__(self):
        return '{s.__class__.__name__} ({s.identifier})'.format(s=self)

    def allowed_phases(self):
        return phases_content.app_phases(self.app)


class ModuleContents:
    _registry = {}

    def __getitem__(self, identifier):
        return self._registry[self._identifier(identifier)]

    def __contains__(self, identifier):
        return self._identifier(identifier) in self._registry

    @classmethod
    def _identifier(cls, identifier):
        if type(identifier) != str:
            raise TypeError('Module identifier must be str')
        if not identifier.endswith(':module'):
            # Assume identfier is just an app label
            return '{app_label}:module'.format(app_label=identifier)
        return identifier

    def register(self, module):
        self._registry[module.identifier] = module

    def as_choices(self):
        return [(identifier, str(module))
                for identifier, module in self._registry.items()]


content = ModuleContents()
