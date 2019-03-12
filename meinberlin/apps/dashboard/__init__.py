from adhocracy4.dashboard import ProjectDashboard
from adhocracy4.dashboard import components
from meinberlin.apps.projects import get_project_type

default_app_config = 'meinberlin.apps.dashboard.apps.Config'


class TypedProjectDashboard(ProjectDashboard):
    def __init__(self, project):
        self.project_type = get_project_type(project)
        if self.project_type == 'bplan':
            project = project.externalproject.bplan
        elif self.project_type == 'external':
            project = project.externalproject
        elif self.project_type == 'container':
            project = project.projectcontainer
        super().__init__(project)

    def get_project_components(self):
        if self.project_type == 'bplan':
            return [components.projects.get('bplan'),
                    components.projects.get('plans'),
                    components.projects.get('adminlog')]
        elif self.project_type == 'external':
            return [components.projects.get('external'),
                    components.projects.get('topics'),
                    components.projects.get('point'),
                    components.projects.get('plans'),
                    components.projects.get('adminlog')]
        elif self.project_type == 'container':
            return [components.projects.get('container-basic'),
                    components.projects.get('container-information'),
                    components.projects.get('topics'),
                    components.projects.get('point'),
                    components.projects.get('plans'),
                    components.projects.get('container-projects')]

        return [component for component in components.get_project_components()
                if component.is_effective(self.project)]

    def get_module_components(self):
        if self.project_type == 'bplan':
            return []
        elif self.project_type == 'external':
            return []
        elif self.project_type == 'container':
            return []

        return components.get_module_components()
