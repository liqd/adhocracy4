from collections import namedtuple

ProjectBlueprint = namedtuple(
    'ProjectBlueprint', [
        'title', 'description', 'content', 'image', 'settings_model'
    ]
)


class DashboardBlueprints:
    _registry = {}

    @property
    def blueprints(self):
        for key, blueprint in self._registry.items():
            yield key, blueprint

    def register(self, key, project_blueprint):
        self._registry[key] = project_blueprint

    def get(self, key):
        return self._registry[key]


blueprints = DashboardBlueprints()
