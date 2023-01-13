import factory

from adhocracy4.test.factories import ProjectFactory
from meinberlin.apps.projectcontainers import models


class ProjectContainerFactory(ProjectFactory):
    class Meta:
        model = models.ProjectContainer

    @factory.post_generation
    def projects(self, create, extracted, **kwargs):
        if not extracted:
            project_factory = factory.SubFactory(ProjectFactory).get_factory()
            self.projects.add(project_factory())

        elif extracted:
            for project in extracted:
                self.projects.add(project)
