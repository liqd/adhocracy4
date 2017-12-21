class PhaseContent():

    features = {}

    @property
    def identifier(self):
        return '{s.app}:{s.phase}'.format(s=self)

    def __str__(self):
        return '{s.__class__.__name__} ({s.app}:{s.phase})'.format(s=self)

    def has_feature(self, feature, model):
        return model in self.features.get(feature, [])


class PhaseContents():
    _registry = {}

    def __getitem__(self, identifier):
        if type(identifier) != str:
            raise TypeError('Phase identifier must be str')
        return self._registry[identifier]

    def __contains__(self, identifier):
        return identifier in self._registry

    def register(self, phase):
        self._registry[phase.identifier] = phase

    def as_choices(self):
        return [(identifier, str(phase))
                for identifier, phase in self._registry.items()]


content = PhaseContents()
