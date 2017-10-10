from django.db import models

from adhocracy4.projects import models as project_models


class ProjectContainer(project_models.Project):
    projects = models.ManyToManyField(
        project_models.Project,
        related_name='containers',
    )

    @property
    def phases(self):
        from adhocracy4.phases import models as phase_models
        return phase_models.Phase.objects\
            .filter(module__project__containers__id=self.id)
