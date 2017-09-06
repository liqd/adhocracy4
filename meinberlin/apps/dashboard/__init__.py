from functools import lru_cache

from meinberlin.apps.dashboard2 import components
from meinberlin.apps.dashboard2 import ProjectDashboard


@lru_cache(maxsize=8)
def get_project_type(project):
    if (hasattr(project, 'externalproject') and
            hasattr(project.externalproject, 'bplan')):
        return 'bplan'
    elif hasattr(project, 'externalproject'):
        return 'external'
    else:
        return 'default'


class TypedProjectDashboard(ProjectDashboard):
    def __init__(self, project):
        self.project_type = get_project_type(project)
        if self.project_type == 'bplan':
            project = project.externalproject.bplan
        elif self.project_type == 'external':
            project = project.externalproject
        super().__init__(project)

    def get_project_components(self):
        if self.project_type == 'bplan':
            return [components.projects.get('bplan')]
        elif self.project_type == 'external':
            return [components.projects.get('external')]

        return [component for component in components.get_project_components()
                if component.is_effective(self.project)]

    def get_module_components(self):
        if self.project_type == 'bplan':
            return []
        elif self.project_type == 'external':
            return []

        return components.get_module_components()
